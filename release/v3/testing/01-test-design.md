# Niko v3 鐪熶汉浣跨敤鍦烘櫙娴嬭瘯璁捐

## 缁撹

v3 鐩稿 `main` 涓嶆槸涓€涓皬琛ヤ竵锛岃€屾槸鎶?Niko 浠庝竴涓崟灞?CLI agent 鎺ㄥ埌浜嗘湰鍦?coding agent runtime harness锛氬叆鍙ｅ眰澶氫簡 TUI/REPL/one-shot 鐨勯€夋嫨锛屾帶鍒跺眰鎷嗗嚭浜?Engine銆乺un artifacts銆乻ession event bus銆乸lan mode銆亀orker manager锛岃兘鍔涘眰澶氫簡 skills銆乼odo銆乻andbox銆乸rovider profile銆佸垎灞傝蹇嗗拰 auto-dream銆?

鎵€浠ヨ繖鎵规祴璇曚笉搴旇缁х画鍙蛋 `Niko(...)` 鍗曞厓瀵硅薄銆傚畠搴旇妯℃嫙浜轰粠缁堢鎵撳紑 Niko銆佽緭鍏ヨ嚜鐒惰瑷€鎴?slash command銆佺‘璁ゅ鎵广€侀€€鍑恒€佹仮澶?session锛岀劧鍚庡啀妫€鏌?`.niko/sessions/`銆乣.niko/runs/`銆佸伐浣滃尯鏂囦欢鍜岀粓绔?TUI 灞曠ず銆?

鏈枃妗ｅ彧璁捐鍦烘櫙锛屼笉瀹炵幇 runner銆?

## 鑼冨洿

### Building

璁捐 50 涓鍒扮鍦烘櫙锛屾瘡涓満鏅兘浠庣敤鎴峰叆鍙ｉ┍鍔?Niko锛?

- Computer Use 鎿嶄綔 macOS Terminal / iTerm / Codex 鍐呯疆缁堢閲岀殑 TUI銆?
- PTY/expect 鎿嶄綔 `uv run niko --repl`锛屾ā鎷熼敭鐩樿緭鍏ャ€佸洖杞︺€佺瓑寰呰緭鍑恒€?
- one-shot CLI 鎿嶄綔 `uv run niko "<prompt>"`锛屾ā鎷熺敤鎴风洿鎺ユ墽琛屼竴娆′换鍔°€?
- 浜嬪悗楠岃瘉鍙妫€鏌?`.niko/sessions/*.json`銆乣.niko/sessions/*.events.jsonl`銆乣.niko/runs/*/{task_state.json,trace.jsonl,report.json}` 鍜屽伐浣滃尯鏂囦欢銆?

### Not Building

- 涓嶅啓 pytest銆乺unner銆乫ixture銆丆omputer Use 鑴氭湰銆?
- 涓嶈窇 50 涓満鏅€?
- 涓嶆彁浜ょ湡瀹?API key锛屼笉鍦ㄦ枃妗ｉ噷鍐欏瘑閽ュ€笺€?
- 涓嶆妸鐜版湁 unit tests 鍏ㄩ儴鏇挎崲鎺夛紱杩欐壒鍦烘櫙鏄汉鏈哄叆鍙ｅ眰鐨?acceptance 琛ュ厖銆?

## v3 鏀瑰姩闈?

浠庡綋鍓?`v3` 鍒嗘敮瀵?`main` 鐨?diff 鐪嬶紝鏍稿績鏀瑰姩瑕嗙洊 111 涓枃浠讹紝绾?12562 琛屾柊澧炪€?310 琛屽垹闄ゃ€傚満鏅璁℃寜浠ヤ笅鑳藉姏闈㈣鐩栵細

| 鏀瑰姩闈?| 浠ｈ〃妯″潡 / 鏂囨。 | 蹇呴』瑕嗙洊鐨勭敤鎴疯涓?|
|---|---|---|
| Engine 涓?run artifacts | `niko_agent/core/engine.py`, `niko_agent/core/runtime.py`, `niko_agent/core/run_store.py` | 涓€娆′换鍔′粠杈撳叆鍒?final 鍏ㄧ▼鍐?session events銆乼race銆乺eport |
| TUI / REPL / one-shot 鍏ュ彛 | `niko_agent/cli.py`, `niko_agent/tui/*` | TTY 榛樿 TUI銆乣--repl` 閫€鍥炴櫘閫?REPL銆乸rompt 鍙傛暟璧?one-shot |
| Slash commands | `niko_agent/commands/slash.py` | `/help`銆乣/session`銆乣/usage`銆乣/context`銆乣/model`銆乣/history`銆乣/resume` 绛?|
| Plan mode | `niko_agent/core/plan_mode.py`, `niko_agent/tools/plan.py` | 鍙兘鍐?active plan artifact锛屾湭鍐欒鍒掍笉鑳?final锛岄€€鍑哄悗鎭㈠ default |
| Tool policy / permission | `niko_agent/core/tool_policy.py`, `niko_agent/core/permissions.py`, `niko_agent/core/tool_executor.py` | read-before-write銆乻hell search 鎷掔粷銆佸鎵?ask/auto/never |
| Sandbox | `niko_agent/features/sandbox/*` | `required` 缂?backend fail closed锛宍best_effort` degrade 鍙 |
| Skills | `niko_agent/features/skills*.py`, `docs/skills.md` | 鍐呯疆 skill銆侀」鐩?skill銆佸弬鏁版浛鎹€乤llowed-tools銆乫ork銆乸rompt-only |
| Subagent / worker | `niko_agent/core/worker_*.py`, `niko_agent/tools/agents.py` | Explore 鍙銆亀orker 鍐?scope銆佺画鎺ャ€佸仠姝€佽鍒掓ā寮忕姝㈠啓 worker |
| Todo ledger | `niko_agent/core/todo_ledger.py`, `niko_agent/tools/todos.py` | todo_add/update/list 鍐欏叆 report 鍜?prompt |
| Memory / auto-dream | `niko_agent/features/memory.py`, `docs/memory.md` | `/remember`銆乣/dream`銆乼opic 鏂囦欢銆乻ecret-shaped 鍐呭鎷掔粷銆乤uto-dream gate |
| Context governance | `niko_agent/core/context_manager.py`, `niko_agent/core/compact.py` | `/compact`銆佽嚜鍔?compact銆乧ontext usage 杩?report |
| Provider profiles | `niko_agent/config/__init__.py`, `niko_agent/providers/clients.py` | OpenAI-compatible銆丄nthropic-compatible銆丏eepSeek profile銆乽sage/cache/error 鍏冩暟鎹?|
| Safety / redaction | `niko_agent/core/runtime_secrets.py`, `niko_agent/core/workspace.py` | path traversal 鎷掔粷銆乻ymlink 瓒婄晫鎷掔粷銆乼race/report 鑴辨晱 |
| Release dogfood | `scripts/run_business_scenario_dogfood.py` | 鐪熷疄涓氬姟浠诲姟璺戝畬鍚庢湁浠ｇ爜銆佹祴璇曘€乺eport銆乼race銆乪vents |

## 鎵ц鏂瑰紡

### 鎺ㄨ崘 runner 褰㈡€?

```
scenario.yaml
  -> 鍒涘缓涓存椂 workspace
  -> 鍚姩 uv run niko --cwd <workspace> --repl 鎴?--tui
  -> Computer Use / PTY 閫愯杈撳叆
  -> 绛夊緟 final / prompt 鍥炴潵
  -> 閫€鍑?Niko
  -> 鍙楠岃瘉宸ヤ綔鍖哄拰 .niko artifacts
```

娴嬭瘯鍏ュ彛蹇呴』鍍忎汉涓€鏍蜂娇鐢?Niko銆傞獙璇佸櫒鍙互鐩存帴璇绘枃浠讹紝浣嗕笉鑳界粫杩囧叆鍙ｅ幓 import `Niko` 璋?runtime 鏂规硶銆?

### 椹卞姩閫夋嫨

| Driver | 鐢ㄩ€?|
|---|---|
| Computer Use | TUI銆佸鎵?prompt銆乤sk_user 閫夋嫨銆乻lash suggestion銆乀erminal 鐪熷疄閿洏琛屼负 |
| PTY/expect | REPL 绋冲畾杈撳叆杈撳嚭銆乣/resume`銆乣/history`銆乣/compact`銆佸杞璇?|
| one-shot CLI | 涓€娆℃€т换鍔°€乸rovider 閰嶇疆銆乺elease smoke銆佸け璐ュ嚭鍙?|
| artifact verifier | 璇诲彇 JSON/JSONL銆佹鏌?changed paths銆乼race events銆乺edaction銆乻ession id |

Computer Use 褰撳墠鐜鍙敤锛涜璁′緷璧栫殑 UI 鍔ㄤ綔鏄?`get_app_state`銆乣type_text`銆乣press_key`銆乣click`銆侾TY 椹卞姩鐢ㄦ湰鏈?shell 鍗冲彲銆?

### 澶栭儴渚濊禆

| 渚濊禆 | 鐢ㄩ€?| 闄嶇骇绛栫暐 |
|---|---|---|
| `uv` | 鍚姩鏈湴 Niko銆佷复鏃?pytest | 娌℃湁 `uv` 鏃跺満鏅爣璁?environment failure |
| Python 3.10+ | Niko 杩愯瑕佹眰 | 浣庣増鏈洿鎺ュけ璐?|
| provider profile / API key | live provider 鍦烘櫙 | 闈?live 鍦烘櫙涓嶄緷璧栵紱live 鍦烘櫙鍙鍙栨湰鍦伴厤缃紝涓嶆妸 key 鍐欒繘浜х墿 |
| Computer Use | TUI/瀹℃壒/ask_user 鍦烘櫙 | PTY 鍙鐩?REPL锛屼絾涓嶈兘鏇夸唬 TUI 鍙琛屼负 |
| bubblewrap | Linux sandbox required 鍦烘櫙 | macOS 涓婇獙璇?required fail closed / best_effort degrade锛屼笉瑕佹眰瀹夎 |

## 閫氳繃鏍囧噯

姣忎釜鍦烘櫙鑷冲皯婊¤冻鍥涚被璇佹嵁锛?

1. 鐢ㄦ埛鍏ュ彛璇佹嵁锛氭湁鐪熷疄 CLI/TUI/REPL 杈撳叆杈撳嚭璁板綍锛屾垨 Computer Use 鎿嶄綔姝ラ銆?
2. 琛屼负璇佹嵁锛氬伐浣滃尯鏂囦欢銆佸懡浠よ緭鍑烘垨 UI 鏂囨湰绗﹀悎棰勬湡銆?
3. Runtime 璇佹嵁锛歚.niko/runs/<run_id>/report.json`銆乣trace.jsonl`銆乣task_state.json` 瀛樺湪涓斿瓧娈垫纭€?
4. Session 璇佹嵁锛歚.niko/sessions/<session_id>.json` 鍜?`.events.jsonl` 璁板綍鍏抽敭浜嬩欢銆?

## 50 涓満鏅?

### 鐪熷疄涓氬姟鍦烘櫙 1-5

| ID | 鍦烘櫙 | Driver | 鐢ㄦ埛鍔ㄤ綔 | 瑕嗙洊 v3 鏀瑰姩 | 楠屾敹璇佹嵁 |
|---|---|---|---|---|---|
| R01 | 瀛︾敓绠＄悊绯荤粺 CRUD 鑴氭墜鏋?| PTY REPL | 鍦ㄧ┖ workspace 杈撳叆鈥滃啓涓€涓鐢熺鐞嗙郴缁燂紝鍖呭惈 Student dataclass銆佸鍒犳敼鏌ャ€乸ytest 娴嬭瘯锛岃窇娴嬭瘯鍚庢€荤粨鈥?| 榛樿 max_steps=50銆乺ead/write/run_shell銆乤rtifact graph銆乿erifier suggestions | `students.py`銆乣tests/test_students.py` 瀛樺湪锛沺ytest pass锛況eport 鏈?changed_paths銆乿erifier_suggestions銆乻tatus completed |
| R02 | 璁㈠崟浠锋牸鎶樻墸 bugfix | one-shot CLI | 鍦ㄥ凡鏈?`src/order_pricing.py` 鍜屽け璐ユ祴璇曚笂杈撳叆鈥滃畾浣嶆姌鎵ｈ绠楅敊璇苟淇锛岃窇 pytest鈥?| read-before-write銆乸atch_file銆乺un_shell銆佺湡瀹炰笟鍔?dogfood | 鍏紡鍙樻垚 `subtotal - discount + tax`锛泃race 鏈?read_file/patch_file/run_shell锛涘閮?pytest pass |
| R03 | 鍙戝竷灏辩华瀹℃煡鎶ュ憡 | PTY REPL + project skill | 鍒涘缓 `.niko/skills/release/SKILL.md`锛岀敤鎴疯緭鍏?`/release billing-api` | project skill銆乤llowed-tools銆亀rite_file銆乻kill_invoked/skill_completed | `reports/release-readiness.md` 鍐欏嚭锛沞vents 鏈?skill_invoked/skill_completed锛涗笟鍔℃枃浠舵湭琚敼 |
| R04 | 绾夸笂浜嬫晠缁帴淇 | PTY REPL 涓ゆ鍚姩 | 绗竴娆¤ Niko 璇讳簨鏁呮祴璇曞苟 `todo_add` 鍚庨€€鍑猴紱绗簩娆?`uv run niko --resume latest --repl` 杈撳叆鈥滅户缁慨澶嶅苟璺戞祴璇曗€?| `/resume`銆乻ession persistence銆乼odo ledger銆乸atch_file銆乺un artifacts | 鍚屼竴 session id锛泃odo_1 done锛沗classify_latency` 淇锛涚浜屾 report 鏈?todos 鍜?todo_changes |
| R05 | 搴撳瓨 CSV 瀵煎叆鍣?| TUI + Computer Use | 鍦?TUI 杈撳叆鈥滃啓搴撳瓨 CSV 瀵煎叆鍣紝璺宠繃鍧忚锛岀敓鎴愭祴璇曪紝杩愯娴嬭瘯鈥濓紝瀹℃壒鍐欐枃浠?| TUI tool card銆乤pproval prompt銆亀rite_file銆乺un_shell銆乫inal rendering | TUI 鍑虹幇 tool card success锛沗inventory_importer.py` 鍜屾祴璇曞瓨鍦紱pytest pass锛沞vents 鏈?permission_decision allow |

### 鍏ュ彛涓庝氦浜掑満鏅?6-14

| ID | 鍦烘櫙 | Driver | 鐢ㄦ埛鍔ㄤ綔 | 瑕嗙洊 v3 鏀瑰姩 | 楠屾敹璇佹嵁 |
|---|---|---|---|---|---|
| S06 | TTY 榛樿杩涘叆 TUI | Computer Use | 鍦?Terminal 鎵ц `uv run niko --cwd <workspace>` | `interaction_mode` 榛樿 TUI | 灞忓箷鏈?Niko TUI status bar锛涙病鏈夌洿鎺ユ墽琛?one-shot |
| S07 | `--repl` 杩涘叆鏅€?REPL | PTY | 鎵ц `uv run niko --cwd <workspace> --repl`锛岃緭鍏?`/help` | REPL fallback銆乻lash help | 杈撳嚭鍚?`Commands:`銆乣/memory`銆乣/subagent` |
| S08 | prompt 鍙傛暟璧?one-shot | one-shot CLI | 鎵ц `uv run niko --cwd <workspace> "鍒楀嚭 README 鎽樿"` | one-shot 鍏ュ彛銆佹棤浜や簰 session | 鍛戒护閫€鍑虹爜涓?0锛況eport status completed锛涙病鏈夌瓑寰?REPL 杈撳叆 |
| S09 | piped stdin 浣跨敤 REPL | PTY | `printf '/help\n/exit\n' | uv run niko --cwd <workspace> --repl` | 闈?TTY 琛屼负 | 杈撳嚭鍛戒护鍒楄〃骞舵甯搁€€鍑?|
| S10 | TUI slash suggestion | Computer Use | TUI 杈撳叆 `/sub`锛屾寜 Tab | `SlashSuggestions`銆乻lash registry | 杈撳叆妗嗗彉鎴?`/subagent `锛泂uggestion 闈㈡澘娑堝け |
| S11 | `/session` 灞曠ず runtime 鐘舵€?| PTY REPL | 杈撳叆 `/plan refactor-auth` 鍚庤緭鍏?`/session` | session command銆乺untime mode銆亀orker summary | 杈撳嚭鍚?session id銆乪vents path銆乺untime mode plan銆乸lan path銆亀orker summary |
| S12 | `/usage` 灞曠ず provider metadata | PTY REPL | 瀹屾垚涓€娆＄畝鍗曚换鍔″悗杈撳叆 `/usage` | usage command銆乸rovider/model/cached tokens 瀛楁 | 杈撳嚭鍚?model銆乥ase url host銆乴ast input/output tokens锛況eport 涓嶆硠闇?key |
| S13 | `/model` 鍙敼褰撳墠 runtime | PTY REPL | 杈撳叆 `/model gpt-test-local`锛屽啀 `/model` | runtime-only model switch | 杈撳嚭 `model: gpt-test-local`锛泈orkspace 娌℃湁鏂板 `.niko.toml` |
| S14 | `/clear` 寮€鏂?session | PTY REPL | 瀹屾垚涓€杞换鍔★紝杈撳叆 `/clear`锛屽啀 `/session` | session lifecycle銆亀orker cleanup | 鏂?session id 涓嶅悓锛涙棫 session 鏂囦欢浠嶅瓨鍦紱current run state 娓呯┖ |

### Plan mode 鍦烘櫙 15-20

| ID | 鍦烘櫙 | Driver | 鐢ㄦ埛鍔ㄤ綔 | 瑕嗙洊 v3 鏀瑰姩 | 楠屾敹璇佹嵁 |
|---|---|---|---|---|---|
| S15 | 璁″垝妯″紡鍙兘鍐?active plan | PTY REPL | `/plan auth-refactor` 鍚庤姹傗€滅洿鎺ユ敼 src/auth.py鈥?| plan tool profile銆亀rite path gate | 杈撳嚭鎷掔粷鍐欐簮鏂囦欢锛沗src/auth.py` 涓嶅瓨鍦ㄦ垨鏈彉锛沞vents 鏈?`plan_mode_path_mismatch` |
| S16 | 鏈啓璁″垝涓嶈兘 final | PTY REPL | `/plan cache` 鍚庤姹傗€滃彧鍙ｅご璇磋鍒掑畬鎴愶紝涓嶅啓鏂囦欢鈥?| `plan_mode.can_finish()` final gate | history 鏈?runtime_notice锛涙渶缁堝繀椤诲啓 `.niko/plans/cache-plan.md` 鎵嶅畬鎴?|
| S17 | absolute plan path 鑷姩褰掍竴 | PTY REPL | `/plan student` 鍚庢彁绀哄啓缁濆璺緞 `<workspace>/.niko/plans/student-plan.md` | plan path normalize | 瀹為檯鍐欏叆 `.niko/plans/student-plan.md`锛涙湭瑙﹀彂瓒婄晫閿欒 |
| S18 | 瓒婄晫 plan path 琚嫆 | PTY REPL | 璁╂ā鍨嬪皾璇曞啓 `.niko/plans/../escape.md` | plan path traversal guard | 杈撳嚭 `plan path must stay`锛泈orkspace 澶栨棤鏂囦欢 |
| S19 | plan mode 鍏佽 Explore 瀛?agent | PTY REPL | `/plan payments` 鍚庤緭鍏?`/subagent explore inspect README` | plan mode + Explore only | worker 瀹屾垚鎴?started锛沺lan mode 淇濇寔锛沞vents 鏈?worker_started/worker_finished |
| S20 | plan mode 绂佹 worker 鍐欏叆 | PTY REPL | `/plan payments` 鍚庤緭鍏?`/subagent worker --scope src change code` | plan mode worker restriction | 杈撳嚭 `plan mode only allows Explore agents`锛沗src/` 鏈敼鍙?|

### 宸ュ叿绛栫暐銆佸鎵逛笌 sandbox 鍦烘櫙 21-29

| ID | 鍦烘櫙 | Driver | 鐢ㄦ埛鍔ㄤ綔 | 瑕嗙洊 v3 鏀瑰姩 | 楠屾敹璇佹嵁 |
|---|---|---|---|---|---|
| S21 | 鏀规枃浠跺墠蹇呴』鍏堣 | one-shot CLI | 瑕佹眰鈥滄妸 README 鐨?world 鏀规垚 niko_agent鈥濓紝浣嗘彁绀轰笉鑳藉厛璇?| prior_read_required | 绗竴娆?patch 琚嫆骞舵彁绀?read_file锛涢殢鍚庤鏂囦欢鍐?patch锛況eport 鏈?rejected reminder |
| S22 | 鏂版枃浠跺彲鐩存帴鍐欙紝瑕嗙洊蹇呴』璇?| PTY REPL | 杈撳叆鈥滄柊寤?notes.txt锛岀劧鍚庤鐩?README.md鈥?| write_file freshness | `notes.txt` 鎴愬姛锛汻EADME 瑕嗙洊鍓嶈鎷掞紝璇诲悗鎵嶅厑璁?|
| S23 | 鑷繁鍒氬啓鐨勬枃浠跺彲 patch | PTY REPL | 杈撳叆鈥滃啓 scripts/check.py 鍚庢妸 False 鏀?True鈥?| self-authored freshness | patch 鎴愬姛锛涙病鏈夐澶?read_file 瑕佹眰 |
| S24 | shell 鎼滅储绫诲懡浠よ鎷?| PTY REPL | 杈撳叆鈥滅敤 grep -R 鎵?TODO鈥?| shell_search_should_use_tool | run_shell 琚嫆锛涙彁绀轰娇鐢?search锛沞vents 鏈?tool_policy_decision deny |
| S25 | pipe 鍚?head/tail/grep 鐢ㄤ簬杈撳嚭绠＄悊鍏佽 | PTY REPL | 杈撳叆鈥滆繍琛?python --version 2>&1 | head -3鈥?| shell policy 绮剧粏鍖?| run_shell exit_code 0锛涗笉琚綋鎴?workspace search |
| S26 | 闀?shell 杈撳嚭钀?artifact | one-shot CLI | 璁?Niko 杩愯杈撳嚭 6000 瀛楃鐨勫懡浠?| output clipping銆乫ull output artifact | tool history 琚鍓紱report/trace 鎸囧悜 full_output_artifact锛沘rtifact 鏂囦欢鍚畬鏁磋緭鍑?|
| S27 | approval `never` 鎷掔粷 risky tool | PTY REPL | `uv run niko --approval never --repl` 鍚庤姹傚啓鏂囦欢 | PermissionChecker single gate | 杈撳嚭 approval denied锛涙枃浠舵湭鍐欙紱events 鏈?permission_decision deny |
| S28 | sandbox required 缂?backend fail closed | one-shot CLI | macOS 涓婃墽琛?`uv run niko --sandbox required "杩愯 echo hi"` | sandbox fail closed | 杈撳嚭 sandbox unavailable锛況eport status failed 鎴?tool_failed锛涙病鏈夐潤榛樼洿璺?|
| S29 | sandbox best_effort degrade 鍙 | one-shot CLI | macOS 涓婃墽琛?`uv run niko --sandbox best_effort "杩愯 echo hi"` | sandbox degrade event | 鍛戒护鎴愬姛杈撳嚭 hi锛沞vents 鏈?sandbox_unavailable |

### Skills 涓庡懡浠ゆ墿灞曞満鏅?30-36

| ID | 鍦烘櫙 | Driver | 鐢ㄦ埛鍔ㄤ綔 | 瑕嗙洊 v3 鏀瑰姩 | 楠屾敹璇佹嵁 |
|---|---|---|---|---|---|
| S30 | `/skills` 涓嶈皟鐢ㄦā鍨?| PTY REPL | 杈撳叆 `/skills` | skill catalog 鏈湴鍒楀嚭 | 杈撳嚭鍚?`/review`銆乣/test`銆乣/commit`銆乣/simplify`锛涙棤鏂?run 鐩綍 |
| S31 | 鍐呯疆 `/review` 甯﹀弬鏁?| PTY REPL | 杈撳叆 `/review focus auth` | bundled skills dynamic arguments | prompt 涓湁 Additional Focus锛沞vents 鏈?skill_invoked |
| S32 | 椤圭洰 skill 鍙傛暟鏇挎崲 | PTY REPL | 鍒涘缓 `.niko/skills/deploy/SKILL.md`锛岃緭鍏?`/deploy staging` | `$ARGUMENTS`銆乣${NIKO_SKILL_DIR}` | final 鎻愬埌 staging锛沞vents 鏈?skill_invoked锛沺rompt 鍚?skill dir |
| S33 | allowed-tools 闄愬埗鍐欐搷浣?| PTY REPL | 鍒涘缓鍙厑璁?`read_file` 鐨?`/readonly` skill锛岀敤鎴疯姹傚畠鍐欐枃浠?| skill allowed_tools | run_shell/write_file 琚嫆锛涚洰鏍囨枃浠朵笉瀛樺湪锛沞vents reason `tool_not_allowed` |
| S34 | fork skill 涓嶆薄鏌撲富 history | PTY REPL | 鍏堣緭鍏ユ櫘閫氭秷鎭紝鍐嶆墽琛?context=fork 鐨?`/inspect README.md` | fork isolated session | 涓?session history 淇濇寔鍘熷璇濓紱events 鏈?skill_completed context fork |
| S35 | prompt-only skill 涓嶅彂妯″瀷璇锋眰 | PTY REPL | 鍒涘缓 `disable-model-invocation: true` 鐨?`/template hello` | prompt-only skill | 鐩存帴杈撳嚭娓叉煋鏂囨湰锛涙棤 model_requested 浜嬩欢 |
| S36 | invalid skill frontmatter 鍙瘖鏂?| PTY REPL | 鍒涘缓缂?`description` 鐨?skill锛岃緭鍏?`/skills` | skill loader robustness | 杈撳嚭涓嶅睍绀哄潖 skill 鎴栧睍绀洪敊璇紱session 涓嶅穿婧?|

### Subagent / worker 鍦烘櫙 37-42

| ID | 鍦烘櫙 | Driver | 鐢ㄦ埛鍔ㄤ綔 | 瑕嗙洊 v3 鏀瑰姩 | 楠屾敹璇佹嵁 |
|---|---|---|---|---|---|
| S37 | Explore 瀛?agent 鍙鎺㈢储 | PTY REPL | `/subagent explore read README and summarize` | Explore child runtime銆乺eadonly profile | worker notification 瀹屾垚锛涙病鏈?workspace changed锛況eport workers 鏈?Explore |
| S38 | worker 鍙兘鍐?scope 鍐?| PTY REPL | `/subagent worker --scope notes create two notes` | worker write_scope | `notes/` 鍐呮枃浠跺啓鍏ワ紱scope 澶栨枃浠朵笉瀛樺湪 |
| S39 | worker 缁帴鍚屼竴涓?child context | PTY REPL | 鍏堣 worker 鍐?`notes/first.txt`锛屽啀 `send_message` 鍐?`notes/second.txt` | child runtime continuation | 涓や釜閫氱煡閮芥槸 `agent_1`锛涚浜岃疆 prompt 鍖呭惈绗竴杞粨鏋?|
| S40 | running worker 涓嶈兘 send_message | PTY/Computer Use | 鍚姩闀夸换鍔?worker锛岃繍琛屼腑杈撳叆缁х画娑堟伅 | running worker guard | 杈撳嚭 `worker is running`锛涙病鏈夊苟鍙戠画鎺?|
| S41 | task_stop 涓 worker | PTY/Computer Use | 鍚姩闃诲 worker 鍚庤緭鍏?`task_stop agent_1` 鎴栧搴旂敤鎴疯姹?| abort propagation | worker status stopped锛沜hild client abort 浜嬩欢鎴?trace stop |
| S42 | `/clear` 鍋滄帀鍚庡彴 worker | PTY REPL | 鍚姩 worker 鍚庤緭鍏?`/clear` | session clear worker cleanup | worker list 娓呯┖锛涙病鏈夋棫 notification 娣峰叆鏂?session |

### Memory銆乧ontext 涓庢仮澶嶅満鏅?43-47

| ID | 鍦烘櫙 | Driver | 鐢ㄦ埛鍔ㄤ綔 | 瑕嗙洊 v3 鏀瑰姩 | 楠屾敹璇佹嵁 |
|---|---|---|---|---|---|
| S43 | `/remember` 鍐?daily log | PTY REPL | 杈撳叆 `/remember 杩欎釜椤圭洰鐢?pytest锛屼笉鐢?unittest` | daily log銆乵emory event | `.niko/memory/logs/YYYY/MM/*.md` 鏈夊唴瀹癸紱events 鏈?memory_note_appended |
| S44 | `/dream` 鍐?topic 鍜?MEMORY.md | PTY REPL + live/model | 鍏?`/remember` 涓夋潯绋冲畾浜嬪疄锛屽啀杈撳叆 `/dream` | dream child run銆乵emory write scope | `.niko/memory/MEMORY.md` 鍜?`topics/*.md` 闈炵┖锛涗笉浼氬啓 memory 澶栨枃浠?|
| S45 | secret-shaped 璁板繂鎷掔粷 | PTY REPL | 杈撳叆鈥滆璁颁綇 API key 鏄?sk-live-secret-abc鈥?| durable promotion reject secret | topic 鏂囦欢涓嶅惈 secret锛況eport 鏈?durable rejection reason secret_shaped |
| S46 | `/compact` 鎵嬪姩鍘嬬缉鍘嗗彶 | PTY REPL | 杩炵画杈撳叆 16 杞暱瀵硅瘽鍚庤緭鍏?`/compact` | manual compaction銆乫uture history shortening | 杈撳嚭 JSON 鏈?pre_tokens > post_tokens锛沞vents 鏈?compaction_created |
| S47 | resume 妫€娴?workspace mismatch | PTY REPL 涓ゆ鍚姩 | 绗竴娆″畬鎴愪换鍔″苟閫€鍑猴紱澶栭儴淇敼鏂囦欢锛涚浜屾 `--resume latest` | checkpoint/runtime identity銆乺esume_state | report prompt_metadata 鏄?partial-stale 鎴?workspace-mismatch锛泃race 鏈?checkpoint_created |

### Provider銆侀敊璇拰瀹¤鍦烘櫙 48-50

| ID | 鍦烘櫙 | Driver | 鐢ㄦ埛鍔ㄤ綔 | 瑕嗙洊 v3 鏀瑰姩 | 楠屾敹璇佹嵁 |
|---|---|---|---|---|---|
| S48 | provider profile 鍒囨崲 | one-shot CLI | 鍒嗗埆鎵ц `--provider openai`銆乣--provider anthropic`銆乣--provider deepseek` 鐨勭煭浠诲姟 | config precedence銆乸rovider client selection | `/usage` 鎴?report 涓?provider_protocol/model 姝ｇ‘锛沚ase_url 宸茶劚鏁忥紱涓嶆硠闇?key |
| S49 | empty provider response 鐢ㄦ埛鍙 | one-shot CLI + fault endpoint | 鐢ㄦ湰鍦板亣 provider 杩斿洖绌哄搷搴旓紝鐢ㄦ埛杈撳叆鈥渉ello鈥?| empty_response retry / failure wording | 鏈€缁堣緭鍑哄惈 `empty_response` 鎴栦腑鏂囩┖鍝嶅簲锛涗笉鍐嶆槸鍐峰啺鍐?`Stopped after model error` |
| S50 | path traversal 涓?secret redaction | one-shot CLI | 瑕佹眰璇诲彇 `../outside` 骞惰繍琛屼細鎵撳嵃 secret 鐨勫懡浠?| workspace safety銆乺edaction | 瓒婄晫璺緞琚嫆锛泃race/report 涓?secret 鍊兼浛鎹负 `<redacted>` |

## 瑕嗙洊鐭╅樀

| 鑳藉姏闈?| 瑕嗙洊鍦烘櫙 |
|---|---|
| TUI / REPL / one-shot | R05, S06-S14 |
| Session events / run artifacts | R01-R05, S08, S11-S14, S26, S37-S42, S47-S50 |
| Plan mode | S15-S20 |
| Tool policy / permission / sandbox | S21-S29 |
| Skills | R03, S30-S36 |
| Subagent / worker | S19-S20, S37-S42 |
| Todo ledger | R04 |
| Memory / auto-dream | S43-S45 |
| Context / compact / resume | S46-S47 |
| Provider profiles / errors / usage | S12, S48-S49 |
| Safety / redaction | S50 |
| 鐪熷疄涓氬姟 workflow | R01-R05 |

## 浼樺厛绾?

鍏堝疄鐜?12 涓渶灏?smoke 鍦烘櫙锛屼綔涓?v3 release gate锛?

1. R01 瀛︾敓绠＄悊绯荤粺 CRUD 鑴氭墜鏋?
2. R02 璁㈠崟浠锋牸鎶樻墸 bugfix
3. R04 绾夸笂浜嬫晠缁帴淇
4. R05 TUI 瀹℃壒鍐欐枃浠?
5. S07 `--repl` + `/help`
6. S15 plan mode 鍙兘鍐?active plan
7. S21 鏀规枃浠跺墠蹇呴』鍏堣
8. S26 闀?shell 杈撳嚭钀?artifact
9. S32 椤圭洰 skill 鍙傛暟鏇挎崲
10. S37 Explore 瀛?agent 鍙鎺㈢储
11. S43 `/remember` 鍐?daily log
12. S50 path traversal 涓?secret redaction

鍐嶈ˉ榻愬墿浣?38 涓満鏅紝褰㈡垚瀹屾暣 v3 acceptance matrix銆?

## 椋庨櫓涓庡彉褰?

### Provider 澶辫触

live provider 鍦烘櫙鍙兘鍥犱负缃戠粶銆侀檺娴佹垨妯″瀷鏍煎紡涓嶇ǔ瀹氬け璐ャ€傝璁′笂鎶?live provider 鍙斁鍦?R02-R04銆丼44銆丼48-S49 绛夊皯鏁板満鏅紱鍏朵綑鍦烘櫙鍙互鐢ㄦ湰鍦板亣 provider 鎴栦弗鏍?prompt 闄嶄綆涓嶇‘瀹氭€с€傚け璐ユ椂涓嶆妸瀹冨綋鎴?runtime 澶辫触锛岄櫎闈?report/trace 娌℃湁璁板綍 provider error銆?

### 50 涓満鏅墽琛屾椂闂磋繃闀?

鍏ㄩ噺璺?50 涓湡浜哄叆鍙ｅ満鏅細鎱€傛渶灏?release gate 鏄?12 涓満鏅紱瀹屾暣濂椾欢鍙互 nightly 鎴栨墜鍔?release 鍓嶈窇銆?

### Computer Use 涓嶇ǔ瀹?

TUI/瀹℃壒/suggestion 鍙兘闈?Computer Use 鎴?Textual 娴嬭瘯鎵嶅儚鐪熶汉銆備负闄嶄綆鑴嗗急鎬э紝Computer Use 鍦烘櫙鍙獙璇佸睆骞曚笂绋冲畾鏂囨湰鍜屾槑纭敭鐩樺姩浣滐紝涓嶄緷璧栧儚绱犵骇鍧愭爣锛汻EPL 鍦烘櫙浼樺厛鐢?PTY銆?

### 鍥炴粴鎴愭湰

鏈枃妗ｅ彧鏄璁★紝鏃犳暟鎹縼绉汇€傚悗缁疄鐜?runner 鏃跺簲璇ユ柊澧炲湪 `tests/human_scenarios/` 鎴?`scripts/run_human_scenarios.py`锛屼笉鏀圭幇鏈?runtime 閫昏緫锛涢渶瑕佸洖婊氭椂鍒犻櫎鏂板娴嬭瘯/鑴氭湰鍗冲彲銆?

## 闇€瑕佽瘎瀹＄殑鍒ゆ柇

鎴戠殑鍒ゆ柇鏄細v3 鐨?acceptance 涓嶅簲璇ヨ拷姹傗€?0 涓兘鏄湡妯″瀷 live call鈥濄€傞偅浼氭祴鍑?provider 鎶栧姩锛屼笉浼氭洿濂藉湴娴嬪嚭 runtime銆傛纭仛娉曟槸鍏ュ彛鐪熶汉鍖栥€佽瘉鎹?runtime 鍖栥€乸rovider live 灏戦噺鎶芥牱銆?

濡傛灉瑕佹帹缈昏繖涓垽鏂紝闇€瑕佽瘉鏄庣湡瀹炴ā鍨嬮殢鏈烘€ф湰韬氨鏄?v3 鐨勪富瑕侀闄╋紝鑰屼笉鏄?Engine銆乼ool policy銆乵emory銆乻ubagent 鍜?artifact 閾捐矾鐨勭ǔ瀹氭€с€?

