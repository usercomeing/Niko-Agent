# Niko v3 鐪熶汉鍦烘櫙娴嬭瘯鍖?

杩欎釜鐩綍鎶?Niko v3 鐩稿 `main` 鐨勭湡浜轰娇鐢ㄥ満鏅祴璇曟暣鐞嗘垚涓€涓彲浠ュ鐩樸€侀噸璺戙€佺户缁墿灞曠殑娴嬭瘯鍖呫€?

瀹冧笉鏄崟鍏冩祴璇曡鏄庯紝涔熶笉鏄?pytest 娓呭崟銆傚畠璁板綍鐨勬槸锛氬儚鐪熷疄鐢ㄦ埛涓€鏍蜂粠 `uv run niko`銆乣--repl`銆乻lash command銆乺esume銆乸rovider profile銆乻kills銆亀orker銆乵emory 绛夊叆鍙ｄ娇鐢?Niko锛岀劧鍚庡彧璇绘鏌?`.niko/runs` 鍜?`.niko/sessions` 浜х墿銆?

## 鐩綍缁撴瀯

| 鏂囦欢 | 鐢ㄩ€?|
|---|---|
| `01-test-design.md` | 50 涓湡浜哄満鏅殑鍘熷璁捐锛岃鐩?v3 鐨?runtime銆丷EPL/TUI銆乸lan mode銆乼ool policy銆乻kills銆乻ubagent銆乵emory銆乸rovider銆佸畨鍏ㄧ瓑鏀瑰姩闈?|
| `02-execution-record.md` | 2026-05-13 鍏ㄩ噺鎵ц璁板綍锛屽寘鍚渶缁?50/50 缁撴灉銆佹毚闇茬殑闂銆佷骇鍝佷慨澶嶅拰楠岃瘉鍛戒护 |
| `03-runner-and-evidence.md` | runner 鎬庝箞璺戙€佽瘉鎹洰褰曟€庝箞鐪嬨€佸浣曞彧璺戝崟鍦烘櫙銆佸浣曞畾浣嶅け璐?|
| `04-scenario-checklist.md` | 50 涓満鏅殑鍒嗙粍妫€鏌ユ竻鍗曪紝鐢ㄤ簬澶嶇洏鍜屽悗缁ˉ璺?|

鐩稿叧浠ｇ爜鍏ュ彛锛?

| 璺緞 | 璇存槑 |
|---|---|
| `scripts/run_v3_human_scenario_gate.py` | 鐪熷疄 CLI/REPL 鍦烘櫙 runner |
| `niko_agent/evaluation/run_evidence.py` | 浠庣湡瀹?`.niko/runs`銆乣.niko/sessions` 璇诲彇璇佹嵁 |
| `tests/test_run_evidence.py` | evidence adapter 鐨勫洖褰掓祴璇?|
| `tests/test_tool_policy_acceptance.py` | 閲嶅宸ュ叿璋冪敤銆乺ead-before-write 绛変骇鍝佸洖褰?|
| `tests/test_permissions_acceptance.py` | plan mode 鍜?permission gate 浜у搧鍥炲綊 |

## 鏈€缁堢姸鎬?

鏈€鍚庝竴娆″共鍑€鍏ㄩ噺缁撴灉锛?

```text
uv run python scripts/run_v3_human_scenario_gate.py --suite full
{"failed": 0, "output_dir": "/private/tmp/niko_agent-v3-human-scenarios/20260513-170838", "passed": 50, "status": "passed"}
```

浠ｇ爜楠岃瘉锛?

```text
uv run ruff check .
All checks passed!

uv run pytest tests -q
224 passed, 2 skipped, 6 warnings in 68.50s
```

## 蹇€熼噸璺?

璺?12 涓紭鍏?gate锛?

```bash
uv run python scripts/run_v3_human_scenario_gate.py
```

璺戝畬鏁?50 鍦烘櫙锛?

```bash
uv run python scripts/run_v3_human_scenario_gate.py --suite full
```

鍙窇鎸囧畾鍦烘櫙锛?

```bash
uv run python scripts/run_v3_human_scenario_gate.py --suite full --scenario S21 --scenario S23
```

鎸囧畾杈撳嚭鐩綍鏃跺繀椤绘斁鍦?Niko repo 澶栵細

```bash
uv run python scripts/run_v3_human_scenario_gate.py --suite full --output-dir /tmp/niko_agent-v3-human-scenarios/manual-run
```

## 澶嶇洏椤哄簭

1. 鍏堣 `02-execution-record.md`锛岀湅鏈€缁堢粨璁哄拰淇繃鐨勯棶棰樸€?
2. 鍐嶈 `03-runner-and-evidence.md`锛岀悊瑙?runner 鎬庝箞妯℃嫙鐪熶汉鍏ュ彛銆佽瘉鎹€庝箞钀界洏銆?
3. 瀵圭収 `04-scenario-checklist.md` 鎵炬煇涓満鏅紝鍐嶅幓鏈€缁堣緭鍑虹洰褰曠湅瀵瑰簲 `logs/`銆乣report.json`銆乣trace.jsonl`銆乣events.jsonl`銆?
4. 濡傛灉瑕佹墿灞曟柊鍦烘櫙锛屽厛琛?`01-test-design.md`锛屽啀琛?`scripts/run_v3_human_scenario_gate.py` 鍜?checklist銆?

## 鍏抽敭鍘熷垯

- 鍦烘櫙蹇呴』浠庣敤鎴峰叆鍙ｉ┍鍔?Niko锛屼笉鑳?import `Niko` 鐩存帴璋?runtime銆?
- 楠岃瘉鍣ㄥ彲浠ヨ鏂囦欢锛屼絾鍙兘璇?Niko 鑷繁鍐欏嚭鐨?artifacts 鍜?scenario workspace銆?
- 杈撳嚭鐩綍蹇呴』鍦?repo 澶栵紝閬垮厤 Niko 鍚戜笂鍙戠幇鐪熷疄 repo root銆?
- live provider 榛樿鐢?DeepSeek锛岄厤缃潵鑷」鐩?`.niko.toml`锛屼笉鎶?key 鍐欒繘鏂囨。鎴栦骇鐗┿€?
- 鍙戠幇浜у搧闂鏃跺厛淇骇鍝侊紝鍐嶈ˉ narrow regression锛涗笉瑕侀€氳繃鏀惧鍦烘櫙鏂█鎺╃洊闂銆?

