# Niko-Agent v1 二次开发完成报告（2026-07-23）

## 结论

《Niko-Agent v1 二次开发计划》中可在本地离线完成的产品目标已经实现并通过完整门禁。当前工作位于隔离工作树 `D:\codex_project\Niko-Agent\.worktrees\niko-v1-completion`，分支为 `work/niko-v1-completion`，没有修改 `main`，没有访问真实 provider，也没有推送远端。

## 计划验收

| 计划项 | 状态 | 主要证据 |
|---|---|---|
| Niko 品牌、包名、唯一 CLI、配置与状态目录 | 完成 | `niko_agent/`、`niko` 入口、`.niko.toml`、`NIKO_*`；CLI smoke 通过 |
| 中英文 README、LICENSE、NOTICE、运行结构说明 | 完成 | `README.md`、`README.en.md`、`LICENSE`、`NOTICE`、`docs/runtime-artifacts.md` |
| 敏感路径与配置脱敏 | 完成 | 原始/解析路径双重校验、预校验 rg 文件清单、父配置隔离、模型/工具/运行证据脱敏回归 |
| `/fork` 与父会话只追加 | 完成 | fork 目标解析、子会话关联与父会话不变回归 |
| checkpoint 与 `/rollback` 两阶段恢复 | 完成 | token 过期/复用、漂移、大小上限、哈希、备份、journal/report、补偿与失败子会话回归 |
| Windows 与跨平台 verifier | 完成 | 阶段超时、自有进程树清理、UTF-8、离线开关、Windows cmd 启动与引号回归 |
| full 离线门禁 | 完成 | 337 passed、5 skipped；Gate8 9/9；deterministic 12/12 |
| 历史 pico 基线复跑 | 无本地材料 | 对象库无 `4adae0b`，本机无 sibling pico 仓库；未虚构结果 |
| 真实 provider smoke / GitHub push | 待授权 | 按计划必须在离线门禁通过后单独请求授权 |

## 主要完成内容

- 将显式 `repo_root_override` 变成不可向父目录穿透的 Git 隔离边界，并贯穿 prefix refresh、worker、evaluator 与 metrics，解决临时目录误继承用户仓库导致的长等待。
- 统一检查点 schema 来源；可信写工具后刷新 workspace identity；runtime identity mismatch 优先 fail closed，且不会请求模型或调用工具。
- 为快照记录排除项、文件数、实际字节数、manifest 与逐文件哈希；超出 16 MiB 单文件或 128 MiB 总量时不产生残缺可恢复快照。
- rollback 预览 token 十分钟有效、一次性消费；确认时复核 workspace、manifest 和文件；恢复前创建备份与 journal，失败时自动补偿并保留脱敏审计报告。
- 将敏感路径策略覆盖 `.env*`、`.niko.toml`、SSH/GPG、AWS/Azure/gcloud/Docker/Kubernetes 凭据与私钥后缀；`.env.example` 等模板例外保持可用。
- 配置加载以实际 workspace 为边界，不再继承父目录 `.env` 或 `.niko.toml`；配置参数中的 provider key 只进入内存脱敏集合。
- 原始模型响应仅在内存中用于解析工具调用；所有 session、trace、report、memory、工具结果与长输出 artifact 在持久化或返回前脱敏。
- Windows shell 使用最小非秘密启动环境，并以显式 `cmd.exe /d /s /c` 禁用用户 AutoRun；兼容清空环境和带空格/引号的命令。
- `scripts/verify.py` 为 Ruff、pytest、acceptance 和 evaluation 设置独立超时；超时只处理本次 verifier 创建的进程树，full 不重复执行 quick 子集。
- 拆分文件工具模块，使注册器重新满足架构行数预算；路径输出统一为 POSIX 风格，Windows/Linux 断言一致。

## 验证证据

本地实现里程碑：

- `53d9e33 feat(recovery): harden workspace recovery and secret boundaries`
- `d8718d6 fix(verify): bound offline gate process lifetime`
- `bceee1a fix(metrics): use timezone-aware capture timestamps`

### 明确边界场景证据

| 计划中的明确场景 | 直接测试证据 |
|---|---|
| fork 的 latest、序号、event_id、turn_id 与父会话只追加 | `test_fork_keeps_workspace_and_parent_session`、`test_fork_accepts_index_event_id_and_turn_id` |
| rollback 先预览、再确认；新文件删除与旧文件恢复 | `test_rollback_requires_preview_and_restores_git_visible_workspace` |
| token 过期、复用和确认参数约束 | `test_rollback_token_expires_and_cannot_be_reused`、`test_rollback_confirm_requires_exactly_one_token` |
| 预览后任意 workspace 漂移拒绝执行 | `test_rollback_refuses_when_workspace_changes_after_preview` |
| 16 MiB 单文件与 128 MiB 总量不生成残缺快照 | `test_oversized_snapshot_is_unavailable_instead_of_partial`、`test_total_snapshot_limit_is_unavailable_instead_of_partial` |
| 敏感、ignored、符号链接排除 | `test_snapshot_excludes_sensitive_files_and_symbolic_links`、敏感路径参数化测试 |
| manifest/文件损坏、非规范路径和 Windows 大小写碰撞 | `test_rollback_rejects_corrupted_snapshot_and_consumes_token`、`test_noncanonical_manifest_paths_are_rejected`、`test_windows_manifest_path_collision_is_rejected` |
| 备份失败、恢复中断、子会话创建后失败与父会话不变 | `test_rollback_backup_failure_does_not_modify_workspace`、`test_rollback_interruption_restores_pre_operation_workspace`、`test_failure_after_child_creation_marks_child_failed_and_restores_parent` |
| required sandbox 无后端时关闭、best_effort 明确降级 | `test_required_sandbox_rejects_when_backend_is_unavailable`、`test_run_shell_best_effort_sandbox_degrades_and_keeps_permission_gate` |
| verifier 超时仅终止本次子进程树 | `test_run_timeout_cleans_only_spawned_process_tree`、`test_windows_cleanup_targets_spawned_pid_tree` |

### Quick gate

命令：

```powershell
D:\codex_project\Niko-Agent\.venv\Scripts\python.exe scripts/verify.py --profile quick
```

结果：Ruff 通过；60 passed，2 skipped，37.13 秒；`Niko-Agent quick verification passed.`

### Full gate

命令：

```powershell
D:\codex_project\Niko-Agent\.venv\Scripts\python.exe scripts/verify.py --profile full
```

结果：

- Ruff：通过。
- 全量 pytest：337 passed，5 skipped，0 warnings，147.68 秒。
- Gate8 real-session acceptance：9 个场景全部通过。
- deterministic evaluation：12/12 通过，失败 0，pass rate 1.0，verifier pass rate 1.0，全部在预算内。
- 总耗时：167.6 秒；最终输出 `Niko-Agent full verification passed.`

### 其他审计

- `python -m niko_agent --help` 正常输出唯一 Niko CLI 参数。
- 当前改动及相对 `feature/niko-v1` 的完整分支差异均通过 `git diff --check`；仅显示 Git 的 LF/CRLF 工作树提示，没有空白错误。
- 对工作区执行常见 AWS、GitHub、OpenAI 与私钥头格式扫描，无真实密钥命中。
- `.niko/`、虚拟环境、缓存和 evaluation 运行产物均未进入待提交文件列表。
- Windows 无符号链接创建权限时，相应用例明确 skip；required sandbox 无后端时 fail closed、best_effort 明确降级的测试通过。

## 已知限制

- 当前 Git 对象库不包含计划指定的 pico 历史提交 `4adae0b`，`D:\codex_project` 下也没有本地 pico 仓库，因此无法重建并复跑未保存的历史基线输出。当前报告只声明 Niko 当前代码门禁，不冒充历史基线证据。
- full gate 有 5 个环境条件 skip：3 个是当前 Windows 主机无符号链接创建权限，2 个是真实 provider/dogfood 默认离线禁用；没有测试警告。
- 当前命令环境没有可用的 `uv` 可执行文件，因此计划中的三个 `uv run ...` 包装命令未原样复跑；其对应的当前虚拟环境 Python 入口、quick/full verifier、CLI smoke 与 deterministic evaluation 均已通过。安装 `uv` 会修改工具环境，需用户授权后执行。
- 早期外层超时留下的 6 个 Python 进程已有 2 个自然结束；PID 26312、35152、35664、44724 仍存在，PID 35152 持续占用约一个 CPU。未获得用户授权前没有终止任何进程。
- 真实 provider 烟测和 GitHub push 尚未执行；两者都需要用户单独明确授权。

## 下一步

1. 单独请求一次最小真实 provider smoke 授权。
2. 单独请求 GitHub push 授权；不直接修改 `main`，不自动创建 PR。
3. 如用户希望清理遗留进程，先复核 PID、可执行路径与启动时间，再只终止上述 4 个 PID。
