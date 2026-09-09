# 本地演示：模型、模式与跨仓库安装修复

- 目标：解决模型切换与缺少 Key、模式切换、仓库外找不到 niko，并完成 PR。
- 起止：2026-09-09，诊断结束采样 16:51，交付完成记录 20:02（Asia/Shanghai）；中途因审查账号额度暂停，19:49 用户要求继续。
- 用户决策：只完善 `/model`，不新增 `/models`；增加 `/mode` 切换并保留旧 plan 命令；执行本机安装并写明不同仓库的用法；完成后提交和创建 PR。
- 边界：用户确认后编辑既有源码 worktree。从 origin/main 建立 codex/fix-local-demo，保留原 work/niko-v2-plan 及其两笔规划提交；不修改既有测试、fixture、历史报告或治理 PR #4。
- 二开结果文档：[本次实现说明](../docs/二开结果文档.md)。

## 诊断与实现

- 真实命令处理器复现：`/model dpsk` 只修改 model 字符串，旧客户端与 factory 未更新；`/mode` 仅查询，参数形式未处理；源码 worktree 能解析项目 Key，根目录默认 OpenAI 且无 Key；仓库外没有可发现入口。
- CLI 装配 ModelSelection：解析已有 profile / alias / 模型名，先创建新连接，成功后更新主连接、后续子 Agent factory、自动输出预算与脱敏集合。配置、构建、prefix 刷新或事件失败时恢复原连接；不回显私有配置解析错误；不持久化模型偏好。
- 初始 CLI/通用 NIKO_* overrides 仅属于初始连接；跨 profile 忽略这些通用覆盖，使用目标专属配置。切回已选 profile 复用其本会话参数；已有子 Agent 保留原连接。
- `/mode plan <主题>`（支持空格）、`/mode default` 委托既有 PlanModeController。旧 `/plan`、`/plan-exit` 保留，错误参数返回用法。
- uv tool install . 安装普通本地包快照（非 editable），入口 C:/Users/jerry wang/.local/bin/niko.exe。后续修改源码需重新安装，分支切换不会自动改变已安装版本。
- 创建此前不存在的 Niko 专属用户配置 ~/.config/niko/config.toml，仅复用本机原有 DeepSeek 项目配置；Key 未回显。没有设置通用用户环境变量，没有覆盖已有文件。

## 修改路径、接口与决策

- niko_agent/cli.py：装配、命令处理与当前 profile 查询。
- niko_agent/model_selection.py：可回退的运行时模型选择。
- niko_agent/config/__init__.py：dpsk 别名、profile 名称、跨 profile 通用覆盖隔离。
- niko_agent/commands/slash.py：帮助与 TUI 提示。
- tests/test_model_mode_switching.py：新增真实 CLI 装配链回归；既有测试不变。
- README.md、docs/configuration.md：独立安装、跨仓库、配置优先级、命令边界；由独立 task 文档切片编辑，与主代理代码和安装工作不重叠。
- lesson.md、progress.txt、docs/二开结果文档.md、本报告：契约、进度与证据。

## 验证命令与证据

使用源码环境 .venv/Scripts/python.exe；pytest 临时根指定为仓库外于源码的短目录 D:/codex_project/Niko-Agent/t/，不提交运行产物。

- 新测试修复前：15 failed / 2 passed，建立红灯；随后新增私有错误脱敏和无 Key 同 profile 兼容覆盖。
- `-m pytest -q tests/test_model_mode_switching.py tests/test_usage.py tests/test_tui.py tests/test_pico.py -p no:cacheprovider --basetemp D:/codex_project/Niko-Agent/t/demo-green2`：112 passed。
- `scripts/verify.py --profile full`：在 Ruff 阶段退出 1，179 项报错与改动前一致。Ruff 0.16.6 默认规则已扩大；排除外部配置继承。未修改门禁、降级工具或批量改写既有源码/测试获得绿灯。
- `-m ruff check --isolated --select E4,E7,E9,F niko_agent tests scripts`：基础错误检查通过，不代替原始 full 门禁失败结果。新增模型选择器和新测试在当前 Ruff 默认规则下均通过。
- `-m pytest -q tests -p no:cacheprovider --basetemp D:/codex_project/Niko-Agent/t/demo-full1`：356 passed, 5 skipped，138.67 秒；5 项为本机不允许 symlink 的跳过。
- `scripts/run_real_session_acceptance.py --output-dir D:/codex_project/Niko-Agent/t/demo-acceptance-20260909`：9/9 passed，NIKO_ACCEPTANCE_LIVE=0。
- `scripts/evaluate.py --deterministic`：12/12 passed，verifier_pass_rate=1.0，预算内 12/12；生成物不提交。
- `uv tool install . --python .venv/Scripts/python.exe`：成功；`uv --no-cache tool list` 显示 niko-agent v0.1.0；PATH 中 niko --help 成功。
- 两个系统临时目录中的独立 Git 仓库：已安装 niko 的 REPL、/model dpsk、/mode plan/default、旧 /plan 与 /plan-exit 均通过；第二个仓库用 --cwd 从第一个仓库启动，session 的 workspace_root 和 .niko 落盘归属正确。初次验收脚本因 Windows 短/长路径字符串不等失败，改用 samefile 核验实际目录后通过，未改产品代码。
- 真实安装包联通：在空白演示仓库以 --provider openai 启动 REPL，执行 /model dpsk，再发送固定无工具探针；返回 NIKO_DEMO_OK，退出码 0，约 4.4 秒。只调用此一条真实探针，无业务源码外发、无响应产物提交。
- 聚合审查首次尝试因账号额度中断；19:49 用户明确要求继续后恢复同一 reviewer，没有新建第二次审查。reviewer 确认 1 项 major：启动导入的专属 `.env` 地址可能覆盖目标 TOML 并与 TOML Key 混用。已在 CLI 保存导入前的进程环境快照，切换解析显式使用该快照；不临时修改全局 os.environ，不改变 .env 后备层。新冲突回归先得到 2 failed / 1 passed，修复后本文件 22 passed。正在重跑全量验证并由同一 reviewer 复查此修复。

### 最终修复验证与安装恢复

- 修复后全量 pytest：359 passed, 5 skipped，149.83 秒，临时根 demo-full2。为避免新增本机用户配置影响既有非隔离测试，此次验证进程的 USERPROFILE 指向隔离测试目录；没有修改任何既有测试。会话验收再次 9/9、确定性评测再次 12/12。当前 Ruff 全量仍为原有 179 项，新增文件默认规则和全库基础规则通过。
- 更新安装包时 Windows 缓存目录的重解析点导致两次 uv 重装失败；已将本任务旧工具环境改名备份，离线重建同一 niko 入口。备份保留于 `C:/Users/jerry wang/AppData/Roaming/uv/niko-agent-backup-20260909-1957`，不进入 uv/tools 扫描，不删除用户数据。
- 最终安装包四个修改源码文件的 SHA256 与源码一致，两个独立演示仓库的已安装 REPL、OpenAI 初始连接到 /model dpsk、/mode plan/default 再次离线通过；没有再消耗真实 API。
- 文档备用入口 `uv tool run --from niko-agent niko --repl` 已离线核验；不能省略 --from，否则 uv 会查找另一个名为 niko 的包。
- 同一 reviewer 对修复完成只读复查：此前 major 已解决并关闭，无新增发现；没有第二次聚合审查。测试数字引用主代理已完成的确定性验证。

## 风险、限制、未完成项

- 命令成功表示本地配置切换成功，不证明远端 Key/模型有效。真实联通仅发送固定非敏感探针，可能产生少量费用。
- 共享 TOML 是所有 Niko 工作区的默认 profile；项目 `.niko.toml` 可覆盖，历史 `.env` 低于 TOML。源码 `.env` 不随安装发布。
- 原始 full 门禁的 179 项 lint 是遗留问题；本次原样报告。全量功能测试结果不能称为整个 full 门禁通过。
- GitHub 认证已验证，既有治理 PR #4 不属于本次范围；不会合并 PR、修改保护规则或清理旧环境。
- Key、用户配置与运行产物不提交。
- 已完成交付：实现提交 `f074c1162a95babbb7d515b5ad63a13e1f5fc620`（`fix: repair model and mode switching for local demos`）已推送；[PR #5](https://github.com/usercomeing/Niko-Agent/pull/5) 为 `codex/fix-local-demo` → `main`，OPEN、非草稿、MERGEABLE，当前无远程检查。未合并。
- 本次文档补充提交：`docs: record local demo PR delivery`，仅记录同一任务的交付状态，不包含行为变更。
- 未完成项：本任务无剩余实现、安装或 PR 创建工作；原始 Ruff 门禁的 179 项既有问题作为已声明限制保留。
- 下一步：用户在目标仓库运行 `niko --repl` 或 `niko --cwd <目标> --repl`；审阅 PR #5，另行安排既有 Ruff 新规则迁移。合并需用户明确确认。
