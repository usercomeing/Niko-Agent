"""工具定义与执行辅助逻辑。

可以把这个文件看成 agent 的能力白名单：模型能申请哪些动作、这些动作
如何做参数校验，以及最终如何执行，都是在这里定义的。
"""

import os
import subprocess
import textwrap
from functools import partial

from pydantic import ValidationError

from ..core.sensitive_paths import require_non_sensitive_path
from .base import RegisteredTool
from .file_tools import (
    is_active_dream_memory_access,
    tool_list_files,
    tool_patch_file,
    tool_read_file,
    tool_search,
    tool_write_file,
)
from .agents import (
    AGENT_TOOL_EXAMPLES,
    AGENT_TOOL_NAMES,
    AGENT_TOOL_SPECS,
    tool_agent,
    tool_send_message,
    tool_task_stop,
    validate_agent_runtime,
)
from .ask_user import (
    ASK_USER_TOOL_EXAMPLES,
    ASK_USER_TOOL_SPECS,
    tool_ask_user,
)
from .plan import (
    PLAN_TOOL_EXAMPLES,
    PLAN_TOOL_SPECS,
    tool_enter_plan_mode,
    tool_exit_plan_mode,
)
from .todos import (
    TODO_TOOL_EXAMPLES,
    TODO_TOOL_SPECS,
    tool_todo_add,
    tool_todo_list,
    tool_todo_update,
)
from .schemas import (
    AgentArgs,
    AskUserArgs,
    EnterPlanModeArgs,
    ExitPlanModeArgs,
    ListFilesArgs,
    PatchFileArgs,
    ReadFileArgs,
    RunShellArgs,
    SearchArgs,
    SendMessageArgs,
    TaskStopArgs,
    TodoAddArgs,
    TodoListArgs,
    TodoUpdateArgs,
    WriteFileArgs,
    first_error_message,
)

_TOOL_SCHEMAS = {
    "list_files": ListFilesArgs,
    "read_file": ReadFileArgs,
    "search": SearchArgs,
    "run_shell": RunShellArgs,
    "write_file": WriteFileArgs,
    "patch_file": PatchFileArgs,
    "todo_add": TodoAddArgs,
    "todo_update": TodoUpdateArgs,
    "todo_list": TodoListArgs,
    "agent": AgentArgs,
    "send_message": SendMessageArgs,
    "task_stop": TaskStopArgs,
    "enter_plan_mode": EnterPlanModeArgs,
    "exit_plan_mode": ExitPlanModeArgs,
    "ask_user": AskUserArgs,
}

BASE_TOOL_SPECS = {
    "list_files": {
        "schema": {"path": "str='.'"},
        "risky": False,
        "description": "List files in the workspace.",
    },
    "read_file": {
        "schema": {"path": "str", "start": "int=1", "end": "int=200"},
        "risky": False,
        "description": "Read a UTF-8 file by line range.",
    },
    "search": {
        "schema": {"pattern": "str", "path": "str='.'"},
        "risky": False,
        "description": "Search the workspace with rg or a simple fallback.",
    },
    "run_shell": {
        "schema": {"command": "str", "timeout": "int=20"},
        "risky": True,
        "description": "Run a shell command in the repo root.",
    },
    "write_file": {
        "schema": {"path": "str", "content": "str"},
        "risky": True,
        "description": "Write a text file.",
    },
    "patch_file": {
        "schema": {"path": "str", "old_text": "str", "new_text": "str"},
        "risky": True,
        "description": "Replace one exact text block in a file.",
    },
    **TODO_TOOL_SPECS,
    **AGENT_TOOL_SPECS,
    **PLAN_TOOL_SPECS,
    **ASK_USER_TOOL_SPECS,
}

TOOL_EXAMPLES = {
    "list_files": '<tool>{"name":"list_files","args":{"path":"."}}</tool>',
    "read_file": '<tool>{"name":"read_file","args":{"path":"README.md","start":1,"end":80}}</tool>',
    "search": '<tool>{"name":"search","args":{"pattern":"binary_search","path":"."}}</tool>',
    "run_shell": '<tool>{"name":"run_shell","args":{"command":"uv run --with pytest python -m pytest -q","timeout":20}}</tool>',
    "write_file": '<tool name="write_file" path="binary_search.py"><content>def binary_search(nums, target):\n    return -1\n</content></tool>',
    "patch_file": '<tool name="patch_file" path="binary_search.py"><old_text>return -1</old_text><new_text>return mid</new_text></tool>',
    **TODO_TOOL_EXAMPLES,
    **AGENT_TOOL_EXAMPLES,
    **PLAN_TOOL_EXAMPLES,
    **ASK_USER_TOOL_EXAMPLES,
}


def build_tool_registry(agent):
    # 工具不是动态发现的，而是显式注册的。
    # 这样模型看到的是一个有边界、可审计的动作集合。
    tools = {
        name: RegisteredTool(
            name=name,
            schema=spec["schema"],
            description=spec["description"],
            risky=bool(spec["risky"]),
            runner=partial(_TOOL_RUNNERS[name], agent),
        )
        for name, spec in BASE_TOOL_SPECS.items()
    }
    return tools


def tool_example(name):
    return TOOL_EXAMPLES.get(name, "")


def validate_tool(agent, name, args):
    args = args or {}

    schema_cls = _TOOL_SCHEMAS.get(name)
    if schema_cls is not None:
        try:
            schema_cls.model_validate(args)
        except ValidationError as exc:
            raise ValueError(first_error_message(exc)) from exc

    # Workspace-aware checks that require the agent (path safety, file state).
    if name in {"list_files", "read_file", "search", "write_file", "patch_file"}:
        raw_path = args.get("path", ".")
        internal_access = _is_active_plan_write(
            agent, name, raw_path
        ) or is_active_dream_memory_access(agent, name, raw_path)
        if not internal_access:
            require_non_sensitive_path(raw_path)
            resolved_path = agent.path(raw_path)
            require_non_sensitive_path(resolved_path.relative_to(agent.root))

    if name == "list_files":
        path = agent.path(args.get("path", "."))
        if not path.is_dir():
            raise ValueError("path is not a directory")

    elif name == "read_file":
        path = agent.path(args["path"])
        if not path.is_file():
            raise ValueError("path is not a file")

    elif name == "search":
        agent.path(args.get("path", "."))

    elif name == "write_file":
        path = agent.path(args["path"])
        if path.exists() and path.is_dir():
            raise ValueError("path is a directory")

    elif name == "patch_file":
        # patch_file 故意做得很严格：old_text 必须精确命中且只能出现一次，
        # 这样修改行为才是确定的，失败原因也更容易解释。
        path = agent.path(args["path"])
        if not path.is_file():
            raise ValueError("path is not a file")
        text = path.read_text(encoding="utf-8")
        count = text.count(str(args.get("old_text", "")))
        if count != 1:
            raise ValueError(f"old_text must occur exactly once, found {count}")

    elif name in AGENT_TOOL_NAMES:
        validate_agent_runtime(agent, name, args)


def _is_active_plan_write(agent, name, raw_path):
    """Allow only Niko's current plan artifact through the .niko guard."""
    if name not in {"write_file", "patch_file"}:
        return False
    if getattr(agent, "runtime_mode", "") != "plan":
        return False
    plan_mode = getattr(agent, "plan_mode", None)
    plan_path = getattr(plan_mode, "plan_path", "")
    if not plan_path:
        return False
    return agent.path(raw_path) == agent.path(plan_path)


def tool_run_shell(agent, args):
    command = str(args.get("command", "")).strip()
    if not command:
        raise ValueError("command must not be empty")
    timeout = int(args.get("timeout", 20))
    if timeout < 1 or timeout > 120:
        raise ValueError("timeout must be in [1, 120]")
    runner = getattr(agent, "sandbox_runner", None)
    if runner is None:
        shell_env = agent.shell_env()
        command_value = command
        use_shell = True
        executable = None
        if os.name == "nt" and shell_env.get("ComSpec"):
            executable = shell_env["ComSpec"]
            command_value = (
                f'{subprocess.list2cmdline([executable])} /d /s /c "{command}"'
            )
            use_shell = False
        result = subprocess.run(
            command_value,
            cwd=agent.root,
            shell=use_shell,
            capture_output=True,
            text=True,
            timeout=timeout,
            executable=executable,
            # 这里传入的是过滤后的环境变量，而不是直接继承整个父 shell 环境，
            # 目的是减少敏感信息被意外带进命令执行环境的风险。
            env=shell_env,
        )
    else:
        result = runner.run(
            command,
            cwd=agent.root,
            env=agent.shell_env(),
            timeout=timeout,
        )
    return textwrap.dedent(
        f"""\
        exit_code: {result.returncode}
        stdout:
        {result.stdout.strip() or "(empty)"}
        stderr:
        {result.stderr.strip() or "(empty)"}
        """
    ).strip()


_TOOL_RUNNERS = {
    "list_files": tool_list_files,
    "read_file": tool_read_file,
    "search": tool_search,
    "run_shell": tool_run_shell,
    "write_file": tool_write_file,
    "patch_file": tool_patch_file,
    "todo_add": tool_todo_add,
    "todo_update": tool_todo_update,
    "todo_list": tool_todo_list,
    "agent": tool_agent,
    "send_message": tool_send_message,
    "task_stop": tool_task_stop,
    "enter_plan_mode": tool_enter_plan_mode,
    "exit_plan_mode": tool_exit_plan_mode,
    "ask_user": tool_ask_user,
}
