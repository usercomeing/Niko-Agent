# 配置

Niko 的配置按下面这个优先级合并：

```
CLI 显式参数 > 进程环境变量 > 项目 .niko.toml > 全局 ~/.config/niko/config.toml > 项目 .env 历史后备 > 代码默认
```

`--config <path>` 完全显式选择一个 TOML 文件，替代全局与项目 TOML 的自动合并；进程环境变量和 CLI 参数仍优先，未指定的值仍可使用 `.env` 历史后备及默认值。

从 Git 仓库子目录启动时，配置和状态边界仍为 Git 根目录。项目 `.niko.toml` 与 `.env` 应放在该根目录；每个仓库的 `.niko/` 独立保存会话、记忆与 checkpoints。

## Provider profile

provider 是 TOML 里的一段配置 profile，名字（如 `deepseek` `openai` `anthropic`）只用于人类辨识；真正决定走哪个协议的是 `protocol` 字段，目前支持 `openai` 和 `anthropic` 两种。

### .niko.toml 示例

放在仓库根目录，**不要提交真实 key**（默认已被 `.gitignore` 忽略）：

```toml
provider = "deepseek"

[providers.deepseek]
protocol = "anthropic"
api_key = "YOUR_DEEPSEEK_API_KEY"
base_url = "https://api.deepseek.com/anthropic/v1"
model = "YOUR_DEEPSEEK_MODEL"

[providers.openai]
protocol = "openai"
api_key = "YOUR_OPENAI_API_KEY"
base_url = "https://api.openai.com/v1"
model = "gpt-5.4"

[providers.anthropic]
protocol = "anthropic"
api_key = "YOUR_ANTHROPIC_API_KEY"
base_url = "https://api.anthropic.com"
model = "claude-sonnet-4-6"
```

请替换占位 Key 和模型名，并使用账号实际可用的 endpoint。真实请求会将请求内容发送到配置的服务商，并可能产生费用。

启动时切 provider：

```bash
niko                       # 用 toml 里的默认 provider
niko --provider openai     # 临时切换
niko --provider anthropic --model claude-opus-4-6
```

### 会话内切换

| 命令 | 行为 |
|------|------|
| `/model` | 显示当前 model、provider 和用法 |
| `/model <model>` | 在当前 provider 内切换模型 |
| `/model <provider> [model]` | 切换 provider profile，可同时指定模型 |

provider 参数支持 `deepseek`（别名 `dpsk`）、`openai`（别名 `gpt`）、`anthropic`（别名 `claude`），以及 TOML 中配置的自定义 profile。单个参数命中 provider 名或别名时优先作为 provider；否则作为当前 provider 的模型名。自定义 profile 必须配置受支持的 `protocol`，并提供其连接所需的 Key、endpoint 和模型。

```text
/model
/model dpsk
/model deepseek <model>
/model openai
/model <custom-profile> <model>
```

跨 provider 时不会继承旧连接的 CLI `--api-key`、`--base-url`、`--model`，也不沿用通用 `NIKO_API_KEY`、`NIKO_BASE_URL`、`NIKO_MODEL`、`NIKO_PROTOCOL` 覆盖值（包括 `.env` 中的同名通用后备）。首次切到目标 provider 时，使用它自己的 profile、专属环境变量和后备配置。

各 provider 在本次运行中保留已选连接和模型；切回初始 provider 时恢复其初始连接参数（包括启动时的 CLI/通用覆盖）及本会话最后选择的模型。跨 provider 若目标缺少 Key，切换失败，原连接保持可用；同 provider 内切换模型仍兼容无需 Key 的本地 endpoint。

会话内切换使用启动时的真实进程环境快照；启动流程后来导入的 `.env` 变量仍保持后备优先级，不会覆盖 TOML 的地址或模型。修改已选 profile 的配置或环境后，请退出并重启 Niko 使新配置生效。

切换仅作用于当前运行及之后新建的子 Agent，已有子 Agent 保持原连接，不写入持久化偏好。切换成功不代表网络鉴权或模型可用性已通过校验，真实请求才验证这些条件。当前没有 `/models` 命令、模型菜单或远端模型列表。

### 运行模式

```text
/mode
/mode plan 梳理当前仓库的测试与发布流程
/mode default
```

`/mode` 查询当前模式；`/mode plan <主题>` 进入 Plan 模式，主题可含空格；`/mode default` 返回默认模式。兼容原有 `/plan <topic> [path]` 和 `/plan-exit`。

## 环境变量

不写 toml 也能跑——只设环境变量即可：

| 变量 | 用途 |
|------|------|
| `NIKO_PROVIDER` | 默认 provider |
| `NIKO_API_KEY` / `NIKO_BASE_URL` / `NIKO_MODEL` / `NIKO_PROTOCOL` | 启动连接的通用 override |
| `ANTHROPIC_API_KEY` / `ANTHROPIC_BASE_URL` / `ANTHROPIC_MODEL` | Anthropic |
| `OPENAI_API_KEY` / `OPENAI_BASE_URL` / `OPENAI_MODEL` | OpenAI |
| `DEEPSEEK_API_KEY` / `DEEPSEEK_BASE_URL` / `DEEPSEEK_MODEL` | DeepSeek |

兼容历史 `.env`：`NIKO_OPENAI_*` / `NIKO_ANTHROPIC_*` / `NIKO_DEEPSEEK_*` 仍然能用。这里的 `.env` 文件作为低于 TOML 的历史后备读取，不等同于高优先级的进程环境变量。共享 TOML 建好后，项目差异请写入项目 `.niko.toml`，不要依赖 `.env` 覆盖共享 TOML。

## 全局配置

Niko 专属全局配置为 `~/.config/niko/config.toml`，Windows 下为 `$HOME/.config/niko/config.toml`。它适合放跨项目共用的 provider profiles，不需要把 Key 写入用户级环境变量。

首次共享 DeepSeek 时，从原项目私有配置复制实际 `api_key`、`base_url`、`model`、`protocol`，并设置顶层 `provider = "deepseek"`。不要将私有配置或真实 Key 提交到 Git。示例中的值仅用于说明格式：

```toml
provider = "deepseek"

[providers.deepseek]
protocol = "anthropic"
api_key = "YOUR_DEEPSEEK_API_KEY"
base_url = "https://api.deepseek.com/anthropic/v1"
model = "YOUR_DEEPSEEK_MODEL"
```

项目 `.niko.toml` 按字段覆盖共享配置，例如仅覆盖当前项目的模型：

```toml
[providers.deepseek]
model = "YOUR_PROJECT_MODEL"
```

## 独立安装与跨仓库使用

在完整源码目录（例如 `D:\src\Niko-Agent`）执行非 editable 安装，建立独立的用户级入口。本机源码目录示例：

```powershell
Set-Location 'D:\codex_project\Niko-Agent\.worktrees\niko-v1-completion'
uv tool install .
uv tool list
niko --help
```

安装会写入用户级工具环境。更新源码后，在同一源码目录执行 `uv tool install --reinstall .`，再运行 `uv tool list` 和 `niko --help` 核验。仅当工具目录缺少 PATH 导致无法找到 `niko` 时，执行 `uv tool update-shell` 后新开终端。

共享配置准备好后，在各目标仓库使用已安装的入口：

```powershell
Set-Location 'D:\projects\repo-A'
niko --repl
# Exit Niko before switching repositories.
Set-Location 'D:\projects\repo-B'
niko --repl
# Or select the target repository without changing the shell directory.
niko --cwd 'D:\projects\repo-B' --repl
```

也可使用 `uv tool run --from niko-agent niko --repl`。包名 `niko-agent` 与命令名 `niko` 不同，必须明确 `--from`，避免 uv 查找另一个名为 `niko` 的包。不推荐目标仓库裸 `uv run niko`，其项目环境可能没有安装该包；不要用 `uv run --directory <源码路径>` 运行其他仓库的任务，以免把配置和状态定位到源码仓库。源码 `.env` 不会随工具安装复制到其他仓库，跨仓库共用连接应通过上述全局配置提供。

## CLI 参数

```bash
niko --provider deepseek --model deepseek-v4-pro
niko --api-key YOUR_API_KEY --base-url https://api.example.com/v1
niko --max-steps 50 --max-new-tokens 4096
niko --temperature 0.0
niko --approval ask          # ask | auto | never
niko --sandbox best_effort   # off | best_effort | required
niko --no-auto-dream         # 关闭后台 memory 整合
niko --cwd /path/to/repo     # 切换工作目录
niko --resume latest         # 续接上一个 session
niko --config /path/to/custom.toml
```

跑 `niko --help` 看完整参数。

## 默认值速查

| 项 | 默认 |
|----|------|
| `max-steps` | 50 |
| `max-new-tokens` | Anthropic 32000 / OpenAI 8192 / DeepSeek 8192 / fallback 4096 |
| `temperature` | 0.2 |
| `approval` | `ask` |
| `sandbox` | `off` |
| `dream-interval` | 24 小时 |
| `dream-min-sessions` | 5 |

## 调试

- `/session` 查看 session 文件路径和当前 runtime 标识
- `/context` 查看上下文用量切片
- `/usage` 查看 token / call 数
- 所有事件流写到 `.niko/sessions/<id>.events.jsonl`，可以用 `tail -f` 观察
- 每次运行的 trace 在 `.niko/runs/<run_id>/trace.jsonl`
