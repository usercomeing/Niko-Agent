# Runner 涓庤瘉鎹鏄?

## Runner 瀹氫綅

`scripts/run_v3_human_scenario_gate.py` 鏄?Niko v3 鐪熶汉鍦烘櫙 runner銆傚畠鍒绘剰璧?Niko 鐨勫叕寮€杩涚▼鍏ュ彛锛?

- one-shot CLI锛歚uv run niko --cwd <workspace> "<prompt>"`
- REPL锛歚uv run niko --cwd <workspace> --repl`
- PTY-style stdin锛氭ā鎷熺敤鎴烽€愯杈撳叆 slash command
- TTY smoke锛氶獙璇侀粯璁?TTY 鍏ュ彛鑳借繘鍏?TUI

runner 涓?import `Niko`锛屼篃涓嶇洿鎺ヨ皟鐢?runtime 鏂规硶銆傚畠鍙垱寤轰复鏃?workspace銆佸惎鍔?Niko 杩涚▼銆佹敹闆?stdout/stderr锛岀劧鍚庤鍙?Niko 鑷繁鍐欏嚭鐨?`.niko` artifacts銆?

## 杈撳嚭鐩綍

榛樿杈撳嚭鐩綍锛?

```text
/tmp/niko_agent-v3-human-scenarios/<YYYYMMDD-HHMMSS>
```

macOS 涓婇€氬父浼氭樉绀轰负锛?

```text
/private/tmp/niko_agent-v3-human-scenarios/<YYYYMMDD-HHMMSS>
```

鐩綍缁撴瀯锛?

```text
<output-dir>/
  summary.json
  summary.md
  logs/
    S21.command.json
    S21.stdout.txt
    S21.stderr.txt
  workspaces/
    s21/
      .git/
      .niko/
        runs/
          run_<timestamp>-<id>/
            task_state.json
            trace.jsonl
            report.json
            artifacts/
        sessions/
          <session>.json
          <session>.events.jsonl
      README.md
```

姣忎釜 scenario workspace 閮戒細鍏?`git init -q`銆傝繖鏄繀瑕佺殑锛歂iko 浼氭牴鎹?git root 璇嗗埆 workspace锛屽鏋滄妸娴嬭瘯鐩綍鏀惧湪 Niko repo 鍐呬笖涓嶅垵濮嬪寲鐙珛 git root锛孨iko 浼氬悜涓婃壘鍒扮湡瀹為」鐩牴鐩綍锛屽鑷存祴璇曟薄鏌?repo銆?

## 甯哥敤鍛戒护

璺?12 涓紭鍏?gate锛?

```bash
uv run python scripts/run_v3_human_scenario_gate.py
```

璺戝畬鏁?50 鍦烘櫙锛?

```bash
uv run python scripts/run_v3_human_scenario_gate.py --suite full
```

鍙窇涓€涓垨澶氫釜鍦烘櫙锛?

```bash
uv run python scripts/run_v3_human_scenario_gate.py --suite full --scenario S21
uv run python scripts/run_v3_human_scenario_gate.py --suite full --scenario S21 --scenario S23
```

浣跨敤鎸囧畾閰嶇疆锛?

```bash
uv run python scripts/run_v3_human_scenario_gate.py --suite full --config /Users/martinlos/code/niko_agent/.niko.toml
```

鎸囧畾杈撳嚭鐩綍锛?

```bash
uv run python scripts/run_v3_human_scenario_gate.py --suite full --output-dir /tmp/niko_agent-v3-human-scenarios/manual-run
```

`--output-dir` 涓嶈兘浣嶄簬 `/Users/martinlos/code/niko_agent` 涓嬮潰銆俽unner 浼氱洿鎺ユ嫆缁濊繖绉嶈矾寰勩€?

## Summary 鎬庝箞鐪?

`summary.json` 鏄満鍣ㄥ彲璇绘眹鎬伙紝鏍稿績瀛楁锛?

```json
{
  "status": "passed",
  "scenario_count": 50,
  "passed": 50,
  "failed": 0,
  "suite": "full",
  "provider": "deepseek",
  "output_dir": "/private/tmp/niko_agent-v3-human-scenarios/20260513-170838"
}
```

姣忎釜 `results[]` 鏉＄洰鍖呭惈锛?

- `id`锛氬満鏅紪鍙凤紝濡?`S21`
- `title`锛氬満鏅爣棰?
- `driver`锛歰ne-shot / REPL / PTY / slash 鐨勫叆鍙ｆ柟寮?
- `status`锛歚passed` 鎴?`failed`
- `checks`锛氬叿浣撻獙鏀堕」
- `commands`锛氬疄闄呮墽琛岀殑 Niko 鍛戒护銆乺eturn code銆乻tdout/stderr 璺緞
- `evidence`锛歳eport銆乼race銆乪vents 璺緞

`summary.md` 鏄粰浜哄揩閫熸祻瑙堢殑琛ㄦ牸锛岄€傚悎澶嶇洏鏃跺厛鎵け璐ュ満鏅拰 evidence 璺緞銆?

## Evidence Adapter

`niko_agent/evaluation/run_evidence.py` 鎻愪緵 `RunEvidence.latest(workspace)`锛屽彧浠庣湡瀹?artifacts 鍙栬瘉锛?

- `.niko/runs/run_*/report.json`
- `.niko/runs/run_*/trace.jsonl`
- `.niko/sessions/*.events.jsonl`

瀹冨皝瑁呯殑鍒ゆ柇鍖呮嫭锛?

- run status / stop reason
- changed paths
- tool events / tool names / tool error codes
- runtime reminders
- long shell output artifacts
- session event 鏄惁鍑虹幇

杩欎箞鍋氭槸涓轰簡閬垮厤 runner 閲屽埌澶勫啓 ad hoc JSON 鏌ヨ锛屼篃閬垮厤鎶婂崟娴嬪唴閮ㄥ璞＄姸鎬佸綋鎴愮湡浜哄満鏅瘉鎹€?

## 澶辫触瀹氫綅娴佺▼

濡傛灉 full suite 澶辫触锛屾寜杩欎釜椤哄簭鐪嬶細

1. 鎵撳紑 `<output-dir>/summary.md`锛屾壘鍒?`failed-check` 琛屻€?
2. 鎵撳紑瀵瑰簲 `logs/<scenario>.stdout.txt` 鍜?`logs/<scenario>.stderr.txt`锛岀湅鐢ㄦ埛鍙琛屼负銆?
3. 鎵撳紑 `workspaces/<scenario>/.niko/runs/<run_id>/report.json`锛岀湅 status銆乻top_reason銆乺untime_reminders銆?
4. 鎵撳紑 `trace.jsonl`锛屾寜 `tool_executed` 鎼滅储 `tool_error_code`銆乣name`銆乣result`銆?
5. 鎵撳紑 `.niko/sessions/*.events.jsonl`锛岀湅 slash command銆乸ermission_decision銆乻kill_invoked銆亀orker 浜嬩欢銆?
6. 鍒ゆ柇鏄骇鍝侀棶棰樸€乺unner 鍙栬瘉闂锛岃繕鏄?live model 娌℃寜鍦烘櫙鎵ц銆?

澶勭悊鍘熷垯锛?

- 浜у搧闂锛氫慨浜у搧浠ｇ爜锛屽啀琛?narrow regression锛屽啀閲嶈窇鐩稿叧 live 鍦烘櫙銆?
- runner 鍙栬瘉闂锛氭妸璇诲彇閫昏緫涓嬫矇鍒?`RunEvidence`锛屼笉瑕佸湪鍦烘櫙閲屾暎鍐欒В鏋愩€?
- live model 鍋忚埅锛氫紭鍏堟敹绱у満鏅?prompt 鎴?step budget锛涗笉瑕佹斁瀹戒骇鍝佽涔夈€?

## 鏈淇杩囩殑鍏抽敭澶辫触

| 鍦烘櫙 | 澶辫触琛ㄧ幇 | 鏍瑰洜 | 淇 |
|---|---|---|---|
| S15 | plan mode 鍧忓啓鍏ラ噸澶嶅埌 step limit | 閲嶅璋冪敤鎷︽埅鍦?permission 鍚庯紝鎷掔粷绫婚噸澶嶈皟鐢ㄦ病鏈夋敹鍙?| repeated guard 鍓嶇Щ鍒?permission/policy 鍓?|
| S21 | 琚?`prior_read_required` 鎷掔粷鍚庯紝琛ヨ鍐嶉噸璇曚粛琚鍒ら噸澶?| 閲嶅瑙勫垯鍙湅鍚屽弬娆℃暟锛屾病鏈夌悊瑙ｂ€滈敊璇悗琛?read鈥?| 鍏佽閿欒璋冪敤鍦ㄥ悓璺緞鎴愬姛 read 鍚庨噸璇?|
| S23 | patch 鎴愬姛鍚庢ā鍨嬪張閲嶆斁鍚屼竴涓?write锛屾妸 True 鍥炴粴鎴?False | 鏂囦欢鏀瑰啓宸ュ叿鍚屽弬鎴愬姛璋冪敤涓嶅簲閲嶆斁 | `write_file/patch_file` 鎴愬姛鍚庡悓鍙傞噸鏀剧洿鎺ユ嫆缁?|
| S18 | `/plan` 闈炴硶璺緞瀵艰嚧 REPL 宕╂簝 | slash command 娌℃崟鑾?path 鏍￠獙寮傚父 | REPL 杩斿洖鐢ㄦ埛鍙 error |
| S26 | 闀?shell 杈撳嚭宸茶惤 artifact 浣?runner 鎵句笉鍒?| artifact 璺緞鍦?trace 鐨?`full_output_artifact` | `RunEvidence.full_output_artifacts()` 缁熶竴璇诲彇 |

## 鏈€缁堣瘉鎹?

鏈€鍚庝竴娆″共鍑€ full suite锛?

```text
/private/tmp/niko_agent-v3-human-scenarios/20260513-170838
```

鏈€缁堝懡浠よ緭鍑猴細

```text
{"failed": 0, "output_dir": "/private/tmp/niko_agent-v3-human-scenarios/20260513-170838", "passed": 50, "status": "passed"}
```

