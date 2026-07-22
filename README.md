# Niko-Agent

轻量、本地、白盒可审计的终端 Coding Agent。

Niko 在当前 Git 仓库中运行，提供 TUI、REPL 和 one-shot CLI；模型提出动作，本地 runtime 负责参数校验、权限判断、敏感路径保护、工具执行和证据落盘。Session、run、checkpoint、memory 与 rollback recovery 全部保存在项目私有目录 `.niko/`。

## 核心能力

- OpenAI-compatible 与 Anthropic-compatible provider profiles。
- 受控文件、搜索、Shell、Todo、Plan 和子 Agent 工具。
- Session resume、checkpoint、`/fork` 和令牌确认的全工作区 `/rollback`。
- `.env`、私钥、云凭据与 `.niko/` 对模型工具不可见。
- Trace、task state、report、session events 与 deterministic evaluation。
- `off`、`best_effort`、`required` 三档 sandbox 策略。

## 安装与启动

要求 Python 3.10+、Git 和 [uv](https://docs.astral.sh/uv/)：

```bash
git clone https://github.com/usercomeing/Niko-Agent.git
cd Niko-Agent
uv sync --dev
uv run niko --help
uv run niko
```

常用入口：

```bash
uv run niko --repl
uv run niko "检查当前仓库最先失败的测试"
uv run niko --resume latest
uv run niko --sandbox best_effort --approval ask
```

## Provider 配置

复制项目模板；真实配置默认被 Git 忽略，并且模型文件工具无法读取：

```bash
cp .niko.toml.example .niko.toml
```

配置优先级：CLI 参数 > `NIKO_*` 环境变量 > `.niko.toml` > 默认值。

```toml
provider = "openai"

[providers.openai]
protocol = "openai"
api_key = ""
base_url = "https://api.openai.com/v1"
model = "gpt-5.4"
```

也可使用 `NIKO_API_KEY`、`NIKO_BASE_URL`、`NIKO_MODEL` 和 `NIKO_PROVIDER`。

## 会话恢复

```text
/history
/resume latest
/fork latest
/rollback latest
/rollback --confirm <preview-token>
```

`/fork` 只截断会话历史，不改变文件。`/rollback` 第一次只返回待创建、修改、删除的文件清单和十分钟有效的一次性令牌；确认时会重新核验工作区指纹，随后先写 recovery 备份再恢复 checkpoint。

快照只覆盖 Git tracked 与非 ignored 文件，永远排除 `.git/`、`.niko/`、ignored 文件、敏感文件和符号链接。单文件上限 16 MiB，单快照上限 128 MiB；超限时 rollback 明确不可用，不产生部分快照。

## 安全边界

- 模型工具不能列出、搜索、读取或改写 `.env*`、`.niko.toml`、SSH/GPG/云凭据、私钥和 `.niko/`。
- `.env.example`、`.env.sample`、`.env.template` 可作为空模板读取。
- Shell 只继承 allowlist 环境变量，trace/report 会脱敏已配置 secret。
- Windows 没有 Bubblewrap。`sandbox=required` 会安全拒绝执行；`best_effort` 会记录降级后继续。不要把 Windows 的 best-effort 称为 OS 级隔离。
- rollback 不处理 ignored 或敏感文件，它们不会被恢复，也不会被删除。

## 验证与评测

默认流程完全离线：

```bash
uv run python scripts/verify.py --profile quick
uv run python scripts/verify.py --profile full
uv run python scripts/evaluate.py --deterministic
```

真实 provider smoke 独立于离线门禁，只有显式设置相应 live flag 才会调用外部 API。

## 项目结构

```text
niko_agent/
├── core/          runtime、engine、session、checkpoint、rollback
├── tools/         工具注册、参数与策略
├── providers/     模型协议适配
├── features/      memory、skills、sandbox
├── evaluation/    指标、benchmark 与 run evidence
└── tui/           Textual 界面
```

更多说明见 `docs/`。许可证和来源见 [LICENSE](LICENSE) 与 [NOTICE](NOTICE)。

