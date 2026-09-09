# Niko-Agent

[English](README.en.md) | 简体中文

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

要求 Python 3.10+、Git 和 [uv](https://docs.astral.sh/uv/)。在完整源码目录中安装独立的用户级入口：

```bash
git clone https://github.com/usercomeing/Niko-Agent.git
cd Niko-Agent
uv tool install .
uv tool list
niko --help
```

已有源码时直接进入源码目录执行上述安装命令。本机完整源码路径示例：

```powershell
Set-Location 'D:\codex_project\Niko-Agent\.worktrees\niko-v1-completion'
uv tool install .
uv tool list
niko --help
```

安装会建立独立工具环境并添加用户级命令；它不是 editable 安装，更新源码后须在源码目录执行 `uv tool install --reinstall .`，再用 `uv tool list` 和 `niko --help` 核验。只有工具目录未加入 PATH、导致找不到 `niko` 时，才执行 `uv tool update-shell`，然后新开终端。

安装后在要处理的仓库启动：

```powershell
Set-Location 'D:\projects\repo-A'
niko --repl
# Exit Niko before switching repositories.
Set-Location 'D:\projects\repo-B'
niko --repl
# Or select the target repository directly.
niko --cwd 'D:\projects\repo-B' --repl
```

也可使用 `uv tool run --from niko-agent niko --repl`。包名是 `niko-agent`，不能省略 `--from` 而让 uv 推断成另一个名为 `niko` 的包。不要用 `uv run --directory <源码路径>` 启动其他仓库的任务，它会把工作目录指向源码；也不推荐在目标仓库直接执行 `uv run niko`，因为该项目环境可能没有安装 Niko。

从子目录启动仍以 Git 根目录作为配置和状态边界。每个仓库各有自己的 `.niko/`，独立保存会话、记忆与 checkpoints。源码目录的 `.env` 不会随工具安装带到其他仓库。

常用入口：

```bash
niko
niko "检查当前仓库最先失败的测试"
niko --resume latest
niko --sandbox best_effort --approval ask
```

## Provider 配置

跨仓库共用的配置放在 Niko 专属 `~/.config/niko/config.toml`；Windows 对应 `$HOME/.config/niko/config.toml`。初次共享 DeepSeek 时，从原项目私有配置中复制实际的 `api_key`、`base_url`、`model` 与 `protocol` 值，设置 `provider = "deepseek"`。以下仅为占位示例，不能原样用于真实请求：

```toml
provider = "deepseek"

[providers.deepseek]
protocol = "anthropic"
api_key = "YOUR_DEEPSEEK_API_KEY"
base_url = "https://api.deepseek.com/anthropic/v1"
model = "YOUR_DEEPSEEK_MODEL"
```

共享配置包含凭据并影响使用它的仓库，请仅在本机保存，不要提交真实 Key。发送模型请求会将请求内容交给配置的服务商，并可能产生费用。

配置优先级：CLI 显式参数 > 进程环境变量 > 项目 `.niko.toml` > 全局 `~/.config/niko/config.toml` > 项目 `.env` 历史后备 > 默认值。`--config <path>` 完全显式选择 TOML 文件，不再合并全局与项目 TOML，环境变量和 CLI 仍优先。

需要项目专属值时，在目标 Git 根目录创建 `.niko.toml`（可参考源码中的 `.niko.toml.example`），覆盖共享值；共享 TOML 建好后，不要依赖 `.env` 覆盖它。通用环境覆盖项包括 `NIKO_API_KEY`、`NIKO_BASE_URL`、`NIKO_MODEL`、`NIKO_PROTOCOL` 和 `NIKO_PROVIDER`。完整示例见 [配置说明](docs/configuration.md)。

## 会话内模型与模式切换

在交互会话中使用：

```text
/model
/model <model>
/model <provider> [model]
/model dpsk
/mode
/mode plan 梳理当前仓库的测试与发布流程
/mode default
```

`/model` 显示当前 model、provider 与用法；`/model <model>` 在当前 provider 内切换模型；参数命中 provider 名时切换对应 profile，可同时指定模型。支持 `dpsk` → `deepseek`、`gpt` → `openai`、`claude` → `anthropic` 别名及 TOML 中的自定义 profile。

跨 provider 不继承旧连接的 CLI 参数或通用 `NIKO_API_KEY/BASE_URL/MODEL/PROTOCOL` 覆盖值。各 provider 保留本次运行中的选择；切回初始 provider 会恢复其连接参数和本会话最后选择的模型。目标缺少 Key 时切换失败并保留原连接；同 provider 内仍兼容无需 Key 的本地 endpoint。切换成功只表示本地连接配置已更新，网络鉴权和模型可用性要到真实请求时才验证。

切换只影响当前运行和之后新建的子 Agent，已有子 Agent 保持原连接，不写入持久化偏好。当前不提供 `/models`、模型菜单或远端模型列表。

`/mode` 查询当前模式，`/mode plan <主题>` 进入 Plan 模式（主题可含空格），`/mode default` 返回默认模式；原有 `/plan <topic> [path]` 和 `/plan-exit` 仍可使用。

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

在源码目录执行 `uv sync --dev` 准备开发环境，随后运行离线验证：

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

更多说明见 `docs/`，运行工件与审计链路见
[docs/runtime-artifacts.md](docs/runtime-artifacts.md)。许可证和来源见
[LICENSE](LICENSE) 与 [NOTICE](NOTICE)。
