# Dream 鍚庡彴璁板繂鏁村悎璁捐

杩欑瘒涓昏鍥炵瓟涓€涓棶棰橈細

**`Niko` 鐨?Dream 鍔熻兘鍒板簳鍦ㄧ郴缁熼噷瑙ｅ喅浠€涔堥棶棰橈紝瀹冪幇鍦ㄦ€庝箞瀹炵幇锛屽拰 Claude Code/Managed Agents 鐨?Dream 璁捐鐩告瘮杩樺樊浠€涔堛€?*

鍏堢粰缁撹銆?

`Niko` 鐜板湪鐨?Dream 涓嶆槸涓诲惊鐜噷鐨勬€濊€冩楠わ紝涔熶笉鏄竴涓畾鏃惰窇鑴氭湰鐨勫澹炽€傚畠鏇村噯纭殑瀹氫綅鏄細**鍦ㄧ敤鎴疯姹傜粨鏉熶箣鍚庯紝鐢ㄤ竴涓彈闄愮殑瀛?`Niko` 瀵?durable memory 鍋氬悗鍙扮淮鎶わ紝鎶婇浂鏁ｆ棩蹇椼€佹棫 topic 鏂囦欢鍜屽巻鍙?session 閲岀殑绋冲畾淇″彿鏁寸悊鎴愪笅涓€娆′細璇濊兘璇绘噦鐨勯暱鏈熻蹇嗐€?*

杩欎欢浜嬬殑闅剧偣涓嶅湪浜庤妯″瀷澶氭€荤粨鍑犲彞璇濄€?

鐪熸鐨勯毦鐐规湁鍥涗釜锛?

1. 闀挎湡璁板繂涓嶈兘鏃犻檺濉炶繘 prompt銆?
2. 璁板繂鍐欏叆涓嶈兘璁╂ā鍨嬭幏寰楁棤闄愭枃浠跺啓鏉冮檺銆?
3. 鏁寸悊璁板繂涓嶈兘闃诲鐢ㄦ埛褰撳墠浠诲姟銆?
4. 鏃ц蹇嗐€侀噸澶嶈蹇嗐€佺煕鐩捐蹇嗗繀椤昏兘琚慨姝ｏ紝鑰屼笉鏄秺绉秺涔便€?

`Niko` 褰撳墠瀹炵幇宸茬粡鎶婅繖鍥涗釜闂鎷嗗紑浜嗭細鐢?`.niko/memory` 鍋氭枃浠跺瀷璁板繂鐩綍锛岀敤 `MEMORY.md` 鍋氬叆鍙ｇ储寮曪紝鐢?`logs/` 鍋?append-only 杈撳叆娴侊紝鐢?`topics/` 鎵挎帴鏁寸悊鍚庣殑涓婚璁板繂锛岀敤 `.consolidate-lock` 鎺у埗鑷姩鏁寸悊鑺傚锛屽啀鐢ㄤ竴涓?`dream` tool profile 鍜?`write_scope` 鎶?Dream 瀛愯繍琛屾椂闄愬埗鍦ㄨ蹇嗙洰褰曞唴銆?

杩欏瀹炵幇宸茬粡寰堟帴杩?Claude Code `autoDream` 鐨勬牳蹇冨舰鎬侊細鍚庡彴 fork 涓€涓彈闄?agent锛岃瀹冭 memory 鍜?transcripts锛屽啀鏇存柊 memory銆傚樊寮備篃寰堟槑纭細Claude Code 鍜?Anthropic Managed Agents 鏇村己璋冨紓姝ヤ换鍔＄敓鍛藉懆鏈熴€佽緭鍑?memory store銆佸彇娑?褰掓。銆乁I 鍙娴嬫€у拰鏇村己鐨勫け璐ュ鐞嗭紱`Niko` 褰撳墠鏇磋交锛岀洿鎺ュ湪鏈湴 memory 鐩綍鍘熷湴鏁寸悊銆?

---

## 涓轰粈涔堥渶瑕?Dream锛岃€屼笉鏄彧闈?`/remember`

濡傛灉鍙湅鍔熻兘琛紝`/remember` 宸茬粡鑳戒繚瀛橀暱鏈熻蹇嗭紝`<memory>...</memory>` 涔熻兘鎶?final answer 閲岀殑鍐呭鍐欒繘 daily log銆傞偅涓轰粈涔堣繕闇€瑕?Dream锛?

鍥犱负淇濆瓨鍜屾暣鐞嗘槸涓や欢涓嶅悓鐨勪簨銆?

`/remember` 瑙ｅ喅鐨勬槸鍏ュ彛闂锛氬綋鍓嶈繖涓€鍒绘湁浠€涔堜笢瑗垮€煎緱璁颁笅鏉ャ€傚畠閫傚悎璁板綍鐢ㄦ埛鏄庣‘瑕佹眰淇濆瓨鐨勫亸濂姐€侀」鐩害瀹氥€佸閮ㄨ祫鏂欎綅缃紝鎴栬€呬竴娆′换鍔＄粨鏉熷悗鍊煎緱娌夋穩鐨勭粨璁恒€?

Dream 瑙ｅ喅鐨勬槸缁存姢闂锛氳繖浜涜褰曡繃涓€娈垫椂闂翠箣鍚庯紝鎬庝箞鍘婚噸銆佸悎骞躲€佷慨姝ｃ€佸垎绫伙紝骞舵妸鐪熸鏈夌敤鐨勫唴瀹规斁鍒版湭鏉?session 鑳藉揩閫熸壘鍒扮殑浣嶇疆銆?

闀挎湡璁板繂濡傛灉娌℃湁鍚庡彴鏁寸悊锛屾渶鍚庝細鍙樻垚涓夌鍧忕姸鎬併€?

绗竴绉嶆槸绱㈠紩鑶ㄨ儉銆俙MEMORY.md` 瓒婂啓瓒婇暱锛屾渶鍚庢瘡娆?session 鍚姩閮借甯︿竴澶ф鍐呭銆侰laude Code 瀹樻柟 memory 鏂囨。閲屼篃鏄庣‘鎶?entrypoint 鎺у埗鍦ㄥ墠 200 琛屾垨 25KB 浠ュ唴锛岃缁嗗唴瀹规斁鍒?topic 鏂囦欢閲屾寜闇€璇诲彇銆俙Niko` 娌跨敤浜嗚繖涓柟鍚戯紝`MEMORY.md` 鏄储寮曪紝涓嶆槸鐭ヨ瘑姝ｆ枃銆?

绗簩绉嶆槸閲嶅鍜岀煕鐩俱€傜敤鎴蜂粖澶╄鐢?`uv`锛屽悗鏉ユ敼鎴?`pipx`锛屽鏋滃彧杩藉姞涓嶆暣鐞嗭紝鏈潵妯″瀷鍚屾椂鐪嬪埌涓や釜鐗堟湰锛屽緢瀹规槗閫夐敊銆侱ream 鐨勪环鍊兼槸鍥炲埌婧愭枃浠朵慨姝ｆ棫浜嬪疄锛岃€屼笉鏄啀琛ヤ竴鏉℃柊浜嬪疄銆?

绗笁绉嶆槸鐬椂鐘舵€佹薄鏌撻暱鏈熻蹇嗐€傚綋鍓嶇洰鏍囥€佷笅涓€姝ャ€佽皟璇曡緭鍑恒€佸け璐ユ爤銆佷复鏃跺懡浠ら兘寰堝儚鏈夌敤淇℃伅锛屼絾瀹冧滑閫氬父涓嶈娲诲埌涓嬩竴鍛ㄣ€傚綋鍓嶄唬鐮侀噷 `reject_durable_reason()` 宸茬粡鏄惧紡杩囨护 secret-shaped 鏂囨湰銆乧heckpoint-like 鍓嶇紑銆侀暱鏃ュ織鍜?stdout/stderr/traceback 杩欑被鍣０锛汥ream prompt 涔熻姹備笉瑕佷繚瀛?transient task state銆?

鎵€浠?Dream 鐨勬牳蹇冭亴璐ｅ彲浠ユ鎷垚涓€鍙ヨ瘽锛?

**鎶婄煭鏈熻緭鍏ユ祦閲岀殑绋冲畾淇″彿锛屾暣鐞嗘垚浣庡櫔澹般€佸彲绱㈠紩銆佸彲淇鐨勯暱鏈熻蹇嗐€?*

---

## 褰撳墠绯荤粺閲?Dream 绔欏湪鍝竴灞?

`Niko` 鐨勮蹇嗙郴缁熺幇鍦ㄥ彲浠ュ垎鎴愪笁灞傘€?

绗竴灞傛槸浼氳瘽鍐呭伐浣滆蹇嗐€?

杩欏眰鐢?`LayeredMemory` 缁存姢锛屼富瑕佹湇鍔″綋鍓?session锛氫换鍔℃憳瑕併€佹渶杩戞枃浠躲€佹枃浠剁煭鎽樿銆佸皯閲?episodic notes銆傚畠瑙ｅ喅鐨勬槸涓嬩竴杞ā鍨嬭皟鐢ㄤ笉瑕侀噸澶嶈鏂囦欢銆佷笉瑕佸繕鎺夊垰鍙戠敓鐨勬搷浣溿€?

绗簩灞傛槸 durable memory 杈撳叆娴併€?

杩欏眰钀藉湪 `.niko/memory/logs/YYYY/MM/YYYY-MM-DD.md`銆俙/remember`銆乫inal answer 閲岀殑 `<memory>` 鏍囩銆佷互鍙婇儴鍒嗘樉寮?durable promotion 閮戒細鎶婂€欓€変俊鎭拷鍔犲埌杩欓噷銆傚畠鏄師濮嬭褰曪紝涓嶈姹傛瘡涓€鏉￠兘绔嬪埢鍙樻垚楂樿川閲忕煡璇嗐€?

绗笁灞傛槸 durable memory 鏁寸悊缁撴灉銆?

杩欏眰鐢?`.niko/memory/MEMORY.md` 鍜?topic 鏂囦欢缁勬垚銆俙MEMORY.md` 鍙繚瀛樼煭绱㈠紩锛宼opic 鏂囦欢淇濆瓨鏈?frontmatter 鐨勭粨鏋勫寲璁板繂銆侰ontextManager 浼氭妸 memory system section 鍜屽綋鍓?`MEMORY.md` 娉ㄥ叆 prompt锛岃妯″瀷鐭ラ亾宸叉湁闀挎湡璁板繂鍦ㄥ摢閲岋紝浠ュ強浠€涔堟椂鍊欒璇诲彇銆?

Dream 灏辩珯鍦ㄧ浜屽眰鍜岀涓夊眰涔嬮棿銆?

瀹冧笉鏄浛浠?`LayeredMemory`锛屼篃涓嶆槸鏇夸唬 `/remember`銆傚畠鏄竴涓淮鎶ゅ伐搴忥細璇诲彇 logs銆佸凡鏈?topic 鏂囦欢鍜屽繀瑕佺殑 session transcript锛屾妸鍊欓€変俊鍙锋暣鐞嗘垚闀挎湡璁板繂銆?

```mermaid
flowchart TD
    U["鐢ㄦ埛璇锋眰"] --> E["Engine 涓诲惊鐜?]
    E --> F["assistant final"]
    F --> P["promote_durable_memory / memory tags"]
    P --> L["logs/YYYY/MM/YYYY-MM-DD.md"]
    F --> G["evaluate_auto_dream_gate"]
    G -->|鏈弧瓒虫椂闂?鏁伴噺闂ㄦ| R["report: skipped"]
    G -->|婊¤冻闂ㄦ| K[".consolidate-lock"]
    K --> T["niko_agent-auto-dream 鍚庡彴绾跨▼"]
    T --> C["鍙楅檺瀛?Niko"]
    C --> DP["build_dream_prompt"]
    DP --> M["璇诲彇 MEMORY.md / topics / logs"]
    DP --> S["绐勮寖鍥存悳绱?session transcripts"]
    M --> W["鏇存柊 topic 鏂囦欢鍜?MEMORY.md"]
    S --> W
    W --> O["dream_consolidated / changed_files / report"]
```

杩欏紶鍥鹃噷鏈€閲嶈鐨勬槸杩愯鏃堕殧绂汇€?

涓?`Niko` 璐熻矗瀹屾垚鐢ㄦ埛浠诲姟銆侱ream 瀛?`Niko` 璐熻矗鏁寸悊 memory銆備袱鑰呭鐢?model client 鍜?session store锛屼絾瀛?`Niko` 鐨?feature flags 浼氬叧闂?`memory` 鍜?`relevant_memory`锛宼ool profile 鍒囧埌 `dream`锛屽啓鍏ヨ寖鍥撮檺鍒跺湪 memory 鐩綍銆?

杩欎釜璁捐閬垮厤浜嗕竴涓父瑙侀棶棰橈細濡傛灉璁╀富寰幆涓€杈规墽琛岀敤鎴蜂换鍔′竴杈规暣鐞嗛暱鏈熻蹇嗭紝prompt 浼氬彉澶嶆潅锛屾潈闄愯竟鐣屼細鍙樻ā绯婏紝澶辫触涔熼毦鍒ゆ柇鍒板簳鏄敤鎴蜂换鍔″け璐ヨ繕鏄蹇嗙淮鎶ゅけ璐ャ€?

---

## 鏁版嵁妯″瀷锛氭枃浠跺瀷 memory store

`Niko` 褰撳墠閫夋嫨鐨勬槸鏂囦欢鍨?durable memory锛岃€屼笉鏄暟鎹簱銆佸悜閲忓簱鎴栦竴寮?JSON 澶ц〃銆?

榛樿鐩綍鏄細

```text
.niko/memory/
鈹溾攢鈹€ MEMORY.md
鈹溾攢鈹€ logs/
鈹?  鈹斺攢鈹€ YYYY/MM/YYYY-MM-DD.md
鈹溾攢鈹€ topics/
鈹?  鈹溾攢鈹€ project-conventions.md
鈹?  鈹溾攢鈹€ key-decisions.md
鈹?  鈹溾攢鈹€ dependency-facts.md
鈹?  鈹斺攢鈹€ user-preferences.md
鈹斺攢鈹€ .consolidate-lock
```

`ensure_memory_dir()` 浼氬垱寤?`logs/`銆乣topics/` 鍜?`MEMORY.md`銆傚鏋滅储寮曚笉瀛樺湪锛岄粯璁ゅ啓鍏ヤ竴娈电┖绱㈠紩璇存槑锛歚/remember` 鍐?daily log锛宍/dream` 鎶?logs 鏁寸悊杩?topic 鏂囦欢銆?

杩欎釜鐩綍鎷嗘硶鏈夊嚑涓伐绋嬩笂鐨勫ソ澶勩€?

### `MEMORY.md` 鏄惎鍔ㄧ储寮?

`MEMORY.md` 鐨勮亴璐ｆ槸璁╂ā鍨嬪揩閫熺煡閬撴湁鍝簺璁板繂鏂囦欢銆佹瘡涓枃浠跺ぇ姒傝В鍐充粈涔堥棶棰樸€?

瀹冧笉搴旇淇濆瓨澶ч噺姝ｆ枃銆傚綋鍓?prompt 閲屾槑纭姹傚畠灏戜簬 200 琛岋紝姣忎竴鏉℃帶鍒跺湪鐭弿杩扮骇鍒€侰laude Code 瀹樻柟 memory 鏂囨。涔熼噰鐢ㄧ被浼煎彛寰勶細entrypoint 鍦?session 鍚姩鏃跺姞杞藉墠 200 琛屾垨 25KB锛岃缁?topic 鏂囦欢鎸夐渶璇诲彇銆?

杩欎釜璁捐鐨勪环鍊兼槸鎺у埗姣忚疆 prompt 鐨勫浐瀹氭垚鏈€?

濡傛灉鎶婃墍鏈夐暱鏈熻蹇嗛兘濉炶繘鍏ュ彛鏂囦欢锛岃蹇嗚秺鏈夌敤锛宲rompt 瓒婇噸锛屾渶鍚庝細鍙嶈繃鏉ラ檷浣?agent 绋冲畾鎬с€傛妸鍏ュ彛鏂囦欢鍋氭垚绱㈠紩锛屽彲浠ヨ闀挎湡璁板繂瑙勬ā澧為暱锛屼絾鍚姩 prompt 浠嶇劧淇濇寔鍙帶銆?

### `logs/` 鏄?append-only 杈撳叆娴?

`logs/YYYY/MM/YYYY-MM-DD.md` 淇濆瓨鐨勬槸鍊欓€変俊鍙枫€?

`append_to_daily_log()` 鍙仛寰堢畝鍗曠殑浜嬶細鎶婃枃鏈?strip 鎺夌┖鐧斤紝鍔犱笂 `HH:MM` 鏃堕棿鎴筹紝杩藉姞鍒板綋澶╂棩蹇楁枃浠躲€?

杩欎釜瀹炵幇鏁呮剰绠€鍗曘€傚叆鍙ｉ樁娈典笉鎬ョ潃鍋氬鏉傚綊绫伙紝鍥犱负鐢ㄦ埛鍒氳瀹屾煇浠朵簨鏃讹紝妯″瀷鏈繀鐭ラ亾瀹冩湭鏉ュ睘浜庡摢涓?topic锛屼篃鏈繀鐭ラ亾瀹冧細涓嶄細琚悗缁簨瀹炴帹缈汇€?

鍏堜繚瀛樹负鏃ュ織锛屽悗闈㈢敱 Dream 鍋氭暣鐞嗭紝杩欐瘮鍏ュ彛澶勭洿鎺ュ啓鍏?topic 鏇寸ǔ銆?

### `topics/` 鏄暣鐞嗗悗鐨勯暱鏈熻蹇?

褰撳墠浠ｇ爜閲屽唴缃簡鍥涗釜榛樿 durable topic锛?

- `project-conventions`
- `key-decisions`
- `dependency-facts`
- `user-preferences`

鍚屾椂 memory system section 閲岃姹傜粨鏋勫寲璁板繂鏂囦欢浣跨敤 frontmatter锛歚name`銆乣description`銆乣type`锛屽叾涓?`type` 鍙兘鏄?`user`銆乣feedback`銆乣project`銆乣reference`銆?

杩欓噷鏈変竴涓€煎緱娉ㄦ剰鐨勮璁＄紳闅欙細榛樿 topic 鍚嶅拰 frontmatter type 鏄袱濂楀垎绫汇€?

杩欎笉鏄繍琛岄敊璇紝浣嗕粠璁捐涓婄湅杩樺彲浠ュ啀鏀舵暃銆倀opic 鏇村儚鏂囦欢缁勭粐鏂瑰紡锛宼ype 鏇村儚璇箟绫诲瀷銆傚悗缁渶濂芥槑纭袱鑰呭叧绯伙紝渚嬪锛?

- `topics/user-preferences.md` 涓昏鎵胯浇 `type: user` 鎴?`type: feedback`
- `topics/key-decisions.md` 涓昏鎵胯浇 `type: project`
- `topics/dependency-facts.md` 涓昏鎵胯浇 `type: reference` 鎴?`type: project`

鍚﹀垯 Dream 瀛?agent 鍦ㄦ柊澧炴枃浠舵椂锛屽彲鑳戒細鍦?topic 鍜?type 涔嬮棿鎽囨憜锛屼骇鐢熻繎浼奸噸澶嶆枃浠躲€?

### `.consolidate-lock` 鍚屾椂鎵挎媴閿佸拰鏃堕棿鎴?

`.consolidate-lock` 鏈変袱涓綔鐢ㄣ€?

绗竴锛屽畠鏄苟鍙戦攣銆傝嚜鍔?Dream 婊¤冻鏉′欢鍚庝細鍏?`try_acquire_lock()`锛岄伩鍏嶅涓悗鍙版暣鐞嗕换鍔″悓鏃舵敼 memory銆?

绗簩锛屽畠鐨?mtime 鏄笂娆℃暣鐞嗘椂闂淬€俙read_last_consolidated_at()` 鐩存帴璇诲彇杩欎釜鏂囦欢鐨勪慨鏀规椂闂达紝`evaluate_auto_dream_gate()` 鐢ㄥ畠璁＄畻璺濈涓婃 consolidation 杩囧幓澶氫箙銆?

杩欎釜璁捐寰?Unix锛氫竴涓湰鍦版枃浠舵壙杞界姸鎬侊紝涓嶉渶瑕侀澶栨湇鍔°€?

浠ｄ环涔熷緢娓呮锛氬鏋?lock 鏂囦欢琚閮ㄦ墜鍔ㄦ敼鍔紝鏃堕棿闂ㄦ鍒ゆ柇浼氳褰卞搷锛涘鏋滆繘绋嬪紓甯搁€€鍑猴紝闇€瑕?stale holder 閫昏緫鍏滃簳銆傚綋鍓嶅疄鐜伴噷 `HOLDER_STALE_S = 3600`锛屼竴灏忔椂鍐呭鏋?holder pid 杩樻椿鐫€灏辫涓洪攣杩樿鍗犵敤锛岃秴杩囨垨 pid 涓嶅瓨鍦ㄥ垯鍏佽鎺ョ銆?

---

## 鍐欏叆璺緞锛氬摢浜涘唴瀹逛細杩涘叆 durable memory

Dream 鍙礋璐ｆ暣鐞嗭紝涓嶅簲璇ユ壙鎷呮墍鏈夊啓鍏ュ叆鍙ｃ€傚綋鍓嶇郴缁熸湁涓夋潯杩涘叆 durable memory 鐨勮矾寰勩€?

### `/remember <text>`

CLI 閲?`/remember` 浼氳皟鐢?`agent.remember_durable_note(note)`锛屽悗鑰呰皟鐢?`append_to_daily_log()`锛屽苟鍚?session event bus 鍙戦€?`memory_note_appended`銆?

杩欐潯璺緞鏈€鐩存帴锛岄€傚悎鐢ㄦ埛鏄惧紡璇磋浣忔煇浠朵簨銆?

瀹冪殑浼樺娍鏄剰鍥炬槑纭紝涓嶉渶瑕佹ā鍨嬩粠涓€澶ф鍥炵瓟閲岀寽鏄笉鏄淇濆瓨銆傚畠鐨勯檺鍒舵槸淇濆瓨绮掑害鍙栧喅浜庣敤鎴疯緭鍏ワ紝閫氬父杩橀渶瑕?Dream 鍚庨潰鏁寸悊銆?

### final answer 閲岀殑 `<memory>` 鏍囩

`maintain_memory_after_turn()` 浼氫粠 final answer 涓彁鍙?`<memory>...</memory>` 鏍囩锛屽苟杩藉姞鍒?daily log銆傝繖涓満鍒堕€傚悎妯″瀷鍦ㄥ畬鎴愪换鍔″悗涓诲姩娌夋穩灏戦噺绋冲畾缁撹銆?

杩欐潯璺緞鐨勯闄╂槸妯″瀷鍙兘杩囧害淇濆瓨銆備负浜嗚В鍐宠繖涓闄╋紝memory system section 閲屽垪浜嗘槑纭殑 not-to-save 瑙勫垯锛氫笉瑕佷繚瀛樺彲浠庝唬鐮?git 鎺ㄥ鍑虹殑鏋舵瀯鍜?API锛屼笉瑕佷繚瀛?recent changes锛屼笉瑕佷繚瀛?secrets銆乺aw command output銆乻tack traces銆佷复鏃?blockers 鍜?next steps銆?

杩欓噷鐨勫師鍒欐槸锛氶暱鏈熻蹇嗗彧淇濆瓨鏈潵 session 璇讳唬鐮佷篃涓嶅鏄撶煡閬撶殑淇℃伅銆?

### `promote_durable_memory()`

涓诲惊鐜湪 final 鎴愬姛鍚庝細璋冪敤 `agent.promote_durable_memory(user_message, final)`銆?

杩欐潯璺緞渚濊禆鐢ㄦ埛璇锋眰閲屽嚭鐜版寔涔呭寲鎰忓浘锛屼緥濡傝嫳鏂囩殑 `remember/save/store/persist`锛屾垨鑰呬腑鏂囩殑 `璁颁綇/淇濆瓨/璁板綍/闀挎湡璁板繂/鎸佷箙璁板繂`銆傜劧鍚庡畠浠?final answer 閲岃瘑鍒浐瀹氬墠缂€琛岋細

- `Project convention: ...`
- `Decision: ...`
- `Dependency: ...`
- `Preference: ...`
- `椤圭洰绾﹀畾锛?..`
- `鍐崇瓥锛?..`
- `渚濊禆锛?..`
- `鍋忓ソ锛?..`

璇嗗埆鍒颁箣鍚庡啀鍋?rejection 妫€鏌ワ紝杩囨护 secret-shaped 鏂囨湰銆乧heckpoint-like 涓存椂鐘舵€併€乻tdout/stderr/traceback 鍜岃繃闀垮櫔澹般€?

杩欐潯璺緞鐨勮璁℃剰鍥炬槸璁?assistant 鍙互鐢ㄥ浐瀹氭牸寮忔妸灏戦噺绋冲畾浜嬪疄鎻愬崌涓?durable memory锛岃€屼笉鏄瘡娆￠兘闈犺嚜鐢辨枃鏈В鏋愩€?

---

## 鑷姩 Dream 浠€涔堟椂鍊欒Е鍙?

鑷姩 Dream 涓嶅簲璇ユ瘡杞兘璺戙€?

姣忚疆閮借窇浼氬甫鏉ヤ笁涓棶棰橈細鎴愭湰楂樸€佽蹇嗚繕娌″舰鎴愯冻澶熷閲忋€佸悗鍙颁换鍔″鏄撳拰鐢ㄦ埛涓嬩竴杞氦浜掓姠璧勬簮銆?

褰撳墠 `Niko` 鐢ㄤ笁涓棬妲涙帶鍒惰嚜鍔ㄨЕ鍙戙€?

### 鏃堕棿闂ㄦ

`dream_interval_hours` 榛樿鏄?24 灏忔椂銆侰LI 鍙傛暟鏄?`--dream-interval`銆?

濡傛灉璺濈涓婃 consolidation 涓嶈冻杩欎釜鏃堕棿锛宍evaluate_auto_dream_gate()` 杩斿洖 `interval_gate`銆?

杩欎釜闂ㄦ瑙ｅ喅鐨勬槸杩囧害鏁寸悊闂銆傝蹇嗘暣鐞嗕笉鏄疄鏃?UI 鏇存柊锛屽畠鏇村儚涓€娆′綆棰戠淮鎶や换鍔°€傛瘡澶╀竴娆℃槸鍚堢悊榛樿鍊笺€?

### session 鏁伴噺闂ㄦ

`dream_min_sessions` 榛樿鏄?5銆侰LI 鍙傛暟鏄?`--dream-min-sessions`銆?

`list_sessions_since()` 浼氭壂鎻?session store 涓?mtime 鏅氫簬涓婃 consolidation 鐨?`.json` 鎴?`.jsonl` 鏂囦欢锛屾帓闄ゅ綋鍓?session锛屽啀缁熻鏁伴噺銆傚鏋滀笉瓒抽槇鍊硷紝杩斿洖 `session_gate`銆?

杩欎釜闂ㄦ瑙ｅ喅鐨勬槸绌鸿窇闂銆傚彧鏈夋椂闂磋繃鍘讳簡浣嗘病鏈夎冻澶熸柊 session锛孌ream 涔熶笉鍊煎緱鍚姩銆?

### 骞跺彂闂ㄦ

鍓嶄袱涓棬妲涙弧瓒冲悗锛宍maintain_memory_after_turn()` 浼氬皾璇曟嬁 `.consolidate-lock`銆?

濡傛灉鎷夸笉鍒帮紝杩斿洖 `lock_held`銆傚鏋滄嬁鍒伴攣锛屽氨鎶婄姸鎬佹爣璁颁负 `submitted`锛屽彂鍑?`auto_dream_started` 浜嬩欢锛屽惎鍔ㄥ悕涓?`niko_agent-auto-dream` 鐨?daemon thread銆?

杩欓噷娌℃湁闃诲涓诲洖绛斻€傜敤鎴峰凡缁忔嬁鍒颁簡 final answer锛屽悗鍙版暣鐞嗙户缁窇銆?

### 鍗曟 session cap

`DREAM_SESSION_CAP = 30`銆傚鏋滃緟鏁寸悊 session 瓒呰繃 30 涓紝`build_dream_prompt()` 鍙垪鏈€杩?30 涓紝骞跺湪 prompt 閲岃鏄庤繖娆″彧澶勭悊鏈€杩戜竴鎵癸紝涓嬩竴娆?Dream 鍐嶇户缁€?

杩欎釜 cap 鏄竴涓疄闄呰繍琛岀粡楠岄┍鍔ㄧ殑淇濇姢銆?

session id 鍒楄〃鏈韩灏变細鍗犱笂涓嬫枃锛宼ranscript 妫€绱篃鍙兘璇卞妯″瀷璇诲彇杩囧鍘嗗彶銆傝繃鍘诲嚭鐜拌繃 Dream prompt 鍥犱负 75+ session id 鎾戠垎涓婁笅鏂囧鑷?provider 杩斿洖 empty response 鐨勯闄╋紝鎵€浠ュ綋鍓嶅疄鐜伴€夋嫨灏忔壒閲忓鐞嗐€?

杩欎篃璇存槑 Dream 涓嶆槸瓒婅椽瓒婂ソ銆傞暱鏈熻蹇嗙淮鎶ゆ洿閫傚悎澧為噺銆佸皬鎵广€佸彲鎭㈠銆?

---

## Dream 瀛愯繍琛屾椂鎬庝箞琚檺鍒朵綇

`run_dream()` 鏄綋鍓嶅姛鑳芥渶鍏抽敭鐨勫嚱鏁般€?

瀹冩病鏈夌洿鎺ュ啓涓€濂楀崟鐙殑 summarizer锛岃€屾槸鍒涘缓涓€涓柊鐨?`Niko` 瀹炰緥锛?

- `model_client` 澶嶇敤鐖?agent銆?
- `workspace` 浠嶇劧鏄綋鍓?repo銆?
- `session_store` 澶嶇敤鐖?agent銆?
- `approval_policy="auto"`銆?
- `max_steps` 鑷冲皯 20銆?
- `max_new_tokens` 鑷冲皯 4096銆?
- `feature_flags` 鍏抽棴 `memory` 鍜?`relevant_memory`銆?
- `write_scope` 鍙寚鍚?memory 鐩綍銆?
- `auto_dream=False`锛岄伩鍏?Dream 閲屽啀瑙﹀彂 Dream銆?
- `set_tool_profile("dream")`銆?

杩欎釜閫夋嫨鐨勫ソ澶勬槸澶嶇敤鐜版湁 runtime銆乼ool executor銆乸ermission checker銆乼race 鍜?model client銆侱ream 涓嶉渶瑕佸彟涓€濂楁墽琛岀郴缁熴€?

浣嗗畠涔熻姹傛潈闄愬眰蹇呴』瓒冲纭€?

### tool profile 鍙粰璇诲拰 memory 鍐?

`build_tool_profiles()` 閲?`dream_tools = read_only | {"write_file", "patch_file"}`銆?

杩欐剰鍛崇潃 Dream 瀛?agent 鍙互璇诲彇宸叉湁璁板繂鍜?transcript锛屽彲浠ュ啓鎴?patch memory 鏂囦欢锛屼絾涓嶈兘璋冪敤 coordinator 宸ュ叿銆乵ode 宸ュ叿銆乮nteractive 宸ュ叿锛屼篃涓嶈兘璺?worker/subagent 缂栨帓銆?

瀹冧笉鏄竴涓畬鏁?agent锛屽彧鏄竴涓彈闄愮淮鎶?agent銆?

### write_scope 鎶婂啓鍏ラ檺鍒跺埌 memory 鐩綍

`PermissionChecker._check_write_scope()` 浼氭妸宸ュ叿璇锋眰閲岀殑 path resolve 鍒?runtime path锛屽啀妫€鏌ュ畠鏄惁钀藉湪 `runtime.write_scope` 鐨勬煇涓?scope 涔嬩笅銆?

Dream 瀛?agent 鐨?`write_scope` 鏄?memory 鐩綍鐩稿 repo root 鐨勮矾寰勩€備篃灏辨槸璇达紝鍗充娇 `approval_policy="auto"`锛宍write_file` 鍜?`patch_file` 涔熷彧鑳藉啓 `.niko/memory` 涓嬬殑鏂囦欢銆?

杩欐槸 Dream 璁捐閲屾渶閲嶈鐨勫畨鍏ㄨ竟鐣屻€?

濡傛灉娌℃湁杩欎釜杈圭晫锛屽悗鍙拌蹇嗘暣鐞嗕换鍔″氨鎷ユ湁浜嗚嚜鍔ㄦ敼浠撳簱浠ｇ爜鐨勮兘鍔涖€傞偅鏍蜂竴鏃?prompt 璇鎴栨ā鍨嬭鍒わ紝Dream 鍙兘鍦ㄧ敤鎴锋病璇锋眰鐨勬椂鍊欐敼涓氬姟鏂囦欢銆傚綋鍓嶅疄鐜版病鏈夎繖涓棶棰樸€?

### Dream 鑷繁涓嶅姞杞?memory

瀛?agent 鐨?`feature_flags` 鍏抽棴浜?`memory` 鍜?`relevant_memory`銆?

杩欑偣瀹规槗琚拷鐣ワ紝浣嗗緢閲嶈銆?

Dream 鐨勪换鍔″氨鏄暣鐞?memory銆傚鏋滃畠鍦ㄨ嚜宸辩殑 prompt 閲屽張鑷姩鍔犺浇褰撳墠 memory system section銆乺elevant memories 鍜屽伐浣滆蹇嗭紝寰堝鏄撻€犳垚寰幆姹℃煋锛氬畠涓€杈规暣鐞?memory锛屼竴杈硅鏃?memory 寮虹儓褰卞搷銆傚綋鍓嶅仛娉曡 Dream prompt 鎴愪负涓昏鎸囦护鏉ユ簮锛屽啀璁╁畠鏄惧紡璇诲彇 memory 鐩綍銆?

杩欎釜璁捐鏇存帴杩戜竴娆″彲鎺х殑缁存姢浠诲姟锛岃€屼笉鏄櫘閫氱敤鎴峰璇濄€?

---

## Dream prompt 涓轰粈涔堝垎鍥涗釜闃舵

`build_dream_prompt()` 鐢熸垚鐨?prompt 鍒嗘垚鍥涗釜闃舵锛?

1. Orient
2. Gather recent signal
3. Consolidate
4. Prune and index

杩欎釜缁撴瀯鍩烘湰瀵瑰簲涓€娆′汉宸ユ暣鐞嗚蹇嗘椂鐨勯『搴忋€?

### Phase 1: Orient

鍏堝垪 memory 鐩綍锛岃 `MEMORY.md`锛屽啀 skim 宸叉湁 topic 鏂囦欢銆?

杩欎竴姝ヨВ鍐抽噸澶嶆枃浠堕棶棰樸€?

濡傛灉涓嶅厛鐪嬪凡鏈夌粨鏋勶紝妯″瀷寰堝鏄撶湅鍒颁竴鏉℃柊鏃ュ織灏卞垱寤轰竴涓柊鏂囦欢锛屾渶鍚?topic 鍙樻垚鍑犲崄涓繎浼兼枃浠躲€侽rient 闃舵瑕佹眰瀹冨厛鐞嗚В鐜扮姸锛屽啀鍐冲畾鏄洿鏂版棫鏂囦欢杩樻槸鏂板鏂囦欢銆?

### Phase 2: Gather recent signal

Prompt 鎶婃潵婧愪紭鍏堢骇鎺掑緱寰堟竻妤氾細

1. daily logs
2. 宸叉湁 memories 閲岀殑婕傜Щ浜嬪疄
3. 蹇呰鏃跺 transcript 鍋氱獎鑼冨洿 grep

杩欓噷鐨勫叧閿槸绐勮寖鍥存悳绱€?

Dream 鏈?transcript dir锛屼絾 prompt 鏄庣‘璇翠笉瑕?exhaustive read锛屼笉瑕佽鏁翠釜 JSONL锛屽彧鍦ㄥ凡缁忔€€鐤戞煇涓俊鎭噸瑕佹椂鐢ㄧ獎璇嶆悳绱€?

杩欏拰 ReAct 璁烘枃閲岀殑 reasoning + acting 鎬濊矾鏄竴鑷寸殑锛氭ā鍨嬩笉鏄彧鍦ㄨ剳鍐呮€荤粨锛屼篃涓嶆槸鐩茬洰璇诲叏閲忕幆澧冿紝鑰屾槸甯︾潃褰撳墠鍒ゆ柇鍘昏皟鐢ㄥ閮ㄥ伐鍏锋嬁璇佹嵁銆傚尯鍒湪浜?ReAct 涓昏璁ㄨ浠诲姟姹傝В杩囩▼锛孌ream 鐢ㄥ湪浠诲姟缁撴潫鍚庣殑璁板繂缁存姢銆?

### Phase 3: Consolidate

杩欎竴姝ヨ姹傛妸鍊煎緱璁颁綇鐨勪俊鎭啓鍏ユ垨鏇存柊 memory 鏂囦欢锛屽悓鏃堕伒瀹?Auto Memory section 鐨勬枃浠舵牸寮忋€乼ype 绾﹀畾鍜?not-to-save 瑙勫垯銆?

杩欓噷鏈€閲嶈鐨勫姩璇嶆槸鏇存柊銆?

闀挎湡璁板繂缁存姢涓嶈兘鍙拷鍔犮€傚畠蹇呴』鑳藉垹闄?contradicted facts锛岃兘鎶?relative dates 杞垚 absolute dates锛岃兘鎶婇噸澶嶆潯鐩悎骞跺埌鍚屼竴涓?topic 鏂囦欢閲屻€?

杩欎篃鏄?Dream 鐩告瘮 `/remember` 鐨勬牳蹇冧环鍊笺€?

### Phase 4: Prune and index

鏈€鍚庢洿鏂?`MEMORY.md`锛屼繚鎸佸畠鐭€佸皬銆佸儚绱㈠紩銆?

Prompt 瑕佹眰姣忎釜 entry 褰㈠锛?

```markdown
- [Title](file.md) - one-line hook
```

骞惰姹傜Щ闄?stale/wrong/superseded 鎸囬拡锛屾妸 verbose index entries 涓嬫矇鍒?topic 鏂囦欢銆?

杩欎竴姝ヨ闀挎湡璁板繂涓嶄細鍥犱负鏈夌敤鑰屽け鎺у闀裤€?

---

## 鍜?Claude Code 褰撳墠璁捐鐨勫搴斿叧绯?

杩欓噷鐨?Claude Code 鍙傝€冩潵鑷袱绫绘潗鏂欙細

1. 瀹樻柟 Claude Code memory 鏂囨。銆?
2. 鏈湴 `civil-engineering-cloud-claude-code-source-v2.1.88/02-claude-code-source-research` 閲岀殑婧愮爜鐮旂┒鏉愭枡銆傚悗鑰呭簲褰撴寜绀惧尯鎭㈠/鐮旂┒鏉愭枡鐞嗚В锛屼笉瑕佸湪闈㈣瘯閲岃鎴愬畼鏂瑰畬鏁村唴閮ㄦ簮鐮併€?

浠庤璁″舰鎬佺湅锛宍Niko` 褰撳墠 Dream 鍜?Claude Code 鐨?`autoDream` 鏈夊嚑澶勬槑鏄惧榻愩€?

### 瀵归綈鐐逛竴锛歁emory directory + entrypoint

Claude Code auto memory 浣跨敤椤圭洰绾?memory directory锛岄噷闈㈡湁 `MEMORY.md` entrypoint 鍜屽涓?topic 鏂囦欢銆俙MEMORY.md` 鏄惎鍔ㄧ储寮曪紝鏈夎鏁板拰瀛楄妭涓婇檺銆?

`Niko` 涔熼噰鐢?`.niko/memory/MEMORY.md + topics/ + logs/`銆?

杩欒鏄?`Niko` 娌℃湁鎶?memory 鍋氭垚涓€娈典笉鏂墿鍐欑殑澶?prompt锛岃€屾槸鎶?memory 褰撴垚涓€涓彲缁存姢鐨勬湰鍦版枃浠剁郴缁熴€?

### 瀵归綈鐐逛簩锛氳嚜鍔ㄦ暣鐞嗘槸鍚庡彴 fork/fork-like agent

Claude Code 婧愮爜鐮旂┒鏉愭枡閲岋紝`autoDream` 浼氬湪婊¤冻 gate 鍚庡垱寤哄悗鍙颁换鍔★紝鐢ㄥ彈闄愬伐鍏烽泦璇诲彇 memory 鍜?transcripts锛屽啀鏇存柊 memory銆?

`Niko` 涔熸槸鍦ㄤ富 turn 缁撴潫鍚庡惎鍔?`niko_agent-auto-dream` daemon thread锛岄噷闈㈠垱寤哄瓙 `Niko` 杩愯 `build_dream_prompt()`銆?

杩欒儗鍚庣殑宸ョ▼鍒ゆ柇涓€鑷达細鐢ㄦ埛浠诲姟鍜岃蹇嗙淮鎶よ鍒嗗紑锛屾暣鐞嗗け璐ヤ笉搴旇鎶婄敤鎴蜂换鍔″彉鎴愬け璐ャ€?

### 瀵归綈鐐逛笁锛氬伐鍏锋潈闄愭敹绐?

Claude Code 鐨?`createAutoMemCanUseTool()` 鍏佽璇荤被宸ュ叿锛屽厑璁?memory 鐩綍鍐呯殑 Edit/Write锛屾嫆缁濆叾浠栧啓鍏ャ€?

`Niko` 鐨勭瓑浠峰疄鐜版槸 `dream` tool profile 鍔?`write_scope`銆?

杩欐瘮鍙湪 prompt 閲屽啓涓€鍙ヤ笉瑕佹敼鍒殑鏂囦欢瑕佸彲闈犮€傛潈闄愯竟鐣岀敱 runtime enforce锛屼笉鐢辨ā鍨嬭嚜瑙変繚璇併€?

### 瀵归綈鐐瑰洓锛氭椂闂淬€乻ession銆乴ock gate

Claude Code autoDream 榛樿涔熸槸绾?24 灏忔椂銆? sessions锛屽苟浣跨敤 consolidation lock 璁板綍 lastConsolidatedAt銆?

`Niko` 閲囩敤 `dream_interval_hours=24.0`銆乣dream_min_sessions=5`銆乣.consolidate-lock` mtime銆?

杩欎釜閫夋嫨璇存槑 Dream 琚綋鎴愪綆棰戠淮鎶や换鍔★紝鑰屼笉鏄瘡杞?summary銆?

---

## 鍜?Claude Code 鐩告瘮锛孨iko 鐜板湪灏戜簡浠€涔?

褰撳墠瀹炵幇宸茬粡鏈夐鏋讹紝浣嗚繕涓嶆槸瀹屾暣鐨?Dream 浜у搧鍖栧舰鎬併€?

### 1. 鎵嬪姩 `/dream` 娌℃湁璧板悓涓€鎶婇攣

鑷姩 Dream 浼氬厛 `try_acquire_lock()`锛屽け璐ュ垯璺宠繃銆?

CLI 閲岀殑 `/dream` 鐩存帴璋冪敤 `agent.run_dream()`銆俙run_dream()` 鍐呴儴浼氬湪缁撴潫鍚?`record_consolidation()`锛屼絾鍚姩鍓嶆病鏈夋嬁 lock銆?

杩欐剰鍛崇潃鎵嬪姩 `/dream` 鍜屽悗鍙?auto dream 鐞嗚涓婂彲鑳藉苟鍙戝啓 memory銆傛鐜囦笉楂橈紝浣嗚繖鏄竴涓湡瀹炶竟鐣屻€?

鏇寸ǔ鐨勫仛娉曟槸鎶?lock acquisition 涓嬫矇鍒?`run_dream()` 鎴栨柊澧炰竴涓?`run_dream_with_lock()`锛岃鎵嬪姩鍜岃嚜鍔ㄥ叡浜悓涓€濂楀苟鍙戞帶鍒躲€傛墜鍔ㄥ懡浠ゅ彲浠ュ甫 `force` 璇箟锛屼絾涔熷簲璇ユ樉寮忓鐞嗗苟鍙戙€?

### 2. 娌℃湁 Dream task 鐢熷懡鍛ㄦ湡瀵硅薄

Claude Code 鐮旂┒鏉愭枡閲屾湁 `DreamTask`锛岃礋璐?UI 鐘舵€併€乧omplete/fail/kill銆乺ollback 绛変换鍔＄敓鍛藉懆鏈熴€?

`Niko` 褰撳墠鍙湁鍚庡彴 thread銆乻ession event bus銆乼race 鍜?`last_memory_maintenance`銆傝繖瀵?CLI harness 宸茬粡澶熺敤锛屼絾濡傛灉瑕佸仛 TUI 鎴栨洿寮虹殑鍙娴嬫€э紝杩樼己涓€涓换鍔″璞★細

- dream id
- pending/running/completed/failed/canceled
- started_at/ended_at
- session_ids
- changed_files
- error
- cancel/kill

娌℃湁杩欎釜瀵硅薄鏃讹紝鐢ㄦ埛鍙兘浠?report 鎴?event 閲岀湅鍒扮粨鏋滐紝涓嶈兘鍍忕鐞嗕竴涓悗鍙颁换鍔￠偅鏍风鐞?Dream銆?

### 3. 娌℃湁杈撳嚭 memory store

Anthropic Managed Agents Dreams 鐨勫畼鏂硅璁℃槸锛氳緭鍏ヤ竴涓?existing memory store 鍜屾渶澶?100 涓?sessions锛孌ream 寮傛鐢熸垚涓€涓柊鐨?output memory store銆傝緭鍏?store 涓嶈淇敼锛岀敤鎴峰彲浠ュ鏌ヨ緭鍑哄悗閫夋嫨浣跨敤鎴栦涪寮冦€?

`Niko` 褰撳墠鏄湪 `.niko/memory` 鍘熷湴淇敼銆?

鍘熷湴淇敼閫傚悎鏈湴 CLI锛氱畝鍗曘€佺洿鎺ャ€佹病鏈夐澶栧瓨鍌ㄧ敓鍛藉懆鏈熴€傜己鐐规槸鍥炴粴鑳藉姏寮便€傝櫧鐒?git 鍙互甯?`.niko` 鏂囦欢鍥炴粴锛屼絾 `.niko` 閫氬父鏈繀杩涚増鏈帶鍒躲€?

濡傛灉鍚庣画鎯虫彁鍗囧彲闈犳€э紝鍙互寮曞叆涓ら樁娈靛啓鍏ワ細

1. Dream 鍐欏埌 `.niko/memory/.dream-runs/<run_id>/output/`
2. 鐢熸垚 diff/report
3. 鐢ㄦ埛鎴栫瓥鐣ョ‘璁ゅ悗 apply 鍒?`.niko/memory`

杩欎細鏇存帴杩?Managed Agents 鐨?output store 鎬濊矾锛屼絾瀹炵幇澶嶆潅搴︿篃鏄庢樉澧炲姞銆?

### 4. 娌℃湁 scan throttle 鍜屽け璐ラ€€閬?

褰撳墠 `evaluate_auto_dream_gate()` 姣忔 turn 鍚庨兘浼氭壂鎻?session store銆備竴鑸儏鍐典笅闂涓嶅ぇ锛屼絾澶у瀷 session 鐩綍閲屽彲浠ヨ€冭檻 scan throttle銆?

Claude Code 鐮旂┒鏉愭枡閲屾湁鏇寸粏鐨?gate 椤哄簭鍜?scan 鎺у埗锛岄伩鍏嶉绻佹壂鎻忓拰棰戠箒澶辫触銆?

`Niko` 鍚庣画鍙互琛ヤ袱浠朵簨锛?

- 璁板綍鏈€杩戜竴娆?session scan 鏃堕棿锛岀煭鏃堕棿鍐呯洿鎺ュ鐢ㄧ粨鏋溿€?
- 瀵硅繛缁け璐ョ殑 Dream 鍋氶€€閬匡紝閬垮厤姣忔婊¤冻 gate 閮介噸澶嶈Е鍙戝悓涓€涓?provider 閿欒銆?

### 5. 娌℃湁鐙珛 session memory 灞?

Claude Code 闄や簡 durable memory锛岃繕鏈?session memory銆乧ompact銆乪xtract memories 绛変笉鍚岀淮鎶ゅ眰銆?

`Niko` 褰撳墠鏈?`LayeredMemory`銆乧ontext compaction 鍜?durable memory锛屼絾 Dream 鐩存帴闈㈠悜 durable memory锛屾殏鏃舵病鏈夌嫭绔嬬殑 session memory markdown銆?

杩欎笉涓€瀹氭槸缂洪櫡銆?

瀵瑰綋鍓?Niko 鐩爣鏉ヨ锛屽厛鎶?durable memory 鍋氱ǔ鏇撮噸瑕併€傜瓑闀夸細璇濆鏉傚害缁х画涓婂崌鏃讹紝鍐嶈€冭檻澧炲姞 session memory 灞傦紝鎶婂崟涓?session 鍐呯殑闀挎湡涓婁笅鏂囧拰璺?session durable memory 鍒嗗紑銆?

---

## 鍜?Managed Agents Dreams 鐨勫叧绯?

Anthropic Managed Agents 瀹樻柟 Dreams 鏂囨。缁欏嚭鐨勫畾涔夊緢鏄庣‘锛欴ream 璁?Claude 鍥為【杩囧幓 sessions锛屾暣鐞?agent memory锛屾竻鐞嗛噸澶嶃€佺煕鐩惧拰杩囨湡鏉＄洰锛屽苟杈撳嚭涓€涓柊鐨?memory store銆?

杩欏 `Niko` 鏈変袱涓洿鎺ュ惎鍙戙€?

绗竴锛孌ream 搴旇琚湅浣?memory store maintenance锛岃€屼笉鏄櫘閫氭€荤粨銆?

鏅€氭€荤粨鍏虫敞鍘嬬缉淇℃伅銆侱ream 鍏虫敞鐨勬槸缁存姢涓€涓湭鏉ヤ細琚户缁娇鐢ㄧ殑 store銆傚畠闇€瑕佸幓閲嶃€佷慨姝ｃ€侀噸缁勩€佽緭鍑哄彲澶嶇敤缁撴瀯銆?

绗簩锛孌ream 搴旇鏈夊紓姝ヤ换鍔＄敓鍛藉懆鏈熴€?

瀹樻柟 Dreams 鏄?pending/running/completed/failed/canceled 鐨勫紓姝ヨ祫婧愶紝鍙互 poll锛屽彲浠ョ湅 usage锛屽彲浠ュ彇娑堬紝鍙互褰掓。銆俙Niko` 褰撳墠宸茬粡鏈夊悗鍙扮嚎绋嬪拰浜嬩欢锛屼絾杩樻病鏈夋妸 Dream 鏆撮湶鎴愪竴绛夎祫婧愩€?

涓嶈繃 `Niko` 涓嶅簲璇ョ収鎼?Managed Agents API銆?

Managed Agents 鏄簯绔?API锛孧emory Store 鏄钩鍙拌祫婧愶紱`Niko` 鏄湰鍦?coding harness锛宮emory 鏄湰鍦版枃浠躲€傜収鎼?output store銆乤rchive銆乥illing銆乺esource id 浼氳瀹炵幇鍙橀噸銆?

鏇村悎閫傜殑杩佺Щ鏂瑰悜鏄惛鏀跺畠鐨勪笁涓伐绋嬪師鍒欙細

1. 杈撳叆鍜岃緭鍑烘渶濂藉彲鍖哄垎锛屾柟渚垮鏌ュ拰鍥炴粴銆?
2. Dream 鏄紓姝ヤ换鍔★紝搴旇鏈夌姸鎬佸拰閿欒銆?
3. 鎴愭湰闅?sessions 鏁伴噺鍜岄暱搴﹀闀匡紝搴旇灏忔壒閲忋€佸彲瑙傚療鍦拌窇銆?

---

## 璁烘枃閲岀殑 memory 鎬濊矾鎬庝箞鏄犲皠鍒?Niko

杩欓儴鍒嗕笉鐢ㄦ妸璁烘枃鑳屾垚鐧剧锛屽彧鎶撳拰 `Niko` Dream 鐩稿叧鐨勮璁″垽鏂€?

### ReAct锛氳鍔ㄥ拰鍒ゆ柇瑕佷氦鏇?

ReAct 鐨勬牳蹇冭础鐚槸璁?LLM 鍦ㄤ换鍔′腑浜ゆ浛鐢熸垚 reasoning traces 鍜?actions锛岄€氳繃澶栭儴鐜鑾峰彇淇℃伅锛屽啀鏇存柊璁″垝鍜屽垽鏂€?

`Niko` 涓诲惊鐜湰韬槸 ReAct 椋庢牸锛氭ā鍨嬫€濊€冧笅涓€姝ワ紝璋冪敤宸ュ叿锛岃缁撴灉锛屽啀鍐冲畾缁х画鎴栫粨鏉熴€?

Dream 缁ф壙鐨勬槸杩欎釜鏂规硶鐨勫悗鍗婇儴鍒嗭細瀹冧笉鏄妯″瀷鍧愬湪 prompt 閲屽嚟璁板繂鎬荤粨锛岃€屾槸缁欏畠璇绘枃浠躲€佹悳绱?transcript銆乸atch memory 鐨勫伐鍏凤紝璁╁畠鍩轰簬璇佹嵁缁存姢璁板繂銆?

杩欓噷鐨勮竟鐣屼篃瑕佽娓呮锛欴ream 涓嶆槸浠诲姟姹傝В agent銆傚畠鐨?actions 琚檺鍒跺湪 memory 缁存姢涓婏紝涓嶈兘鎵╁ぇ鎴?general worker銆?

### Generative Agents锛氳蹇嗛渶瑕?reflection

Generative Agents 璁烘枃閲屾湁涓€涓 agent memory 寰堥噸瑕佺殑缁撴瀯锛氬畬鏁寸粡楠岃褰曘€佸熀浜庢椂闂寸殑鍙嶆€濄€佸姩鎬佹绱紝鍐嶇敤杩欎簺璁板繂鍘昏鍒掕涓恒€?

`Niko` 褰撳墠娌℃湁鍋氬畬鏁寸殑 social simulation锛屼篃娌℃湁鍋氬鏉?planning銆傚畠鍊熼壌鐨勬槸鏇寸獎鐨勪竴鐐癸細缁忛獙璁板綍涓嶈兘鐩存帴绛変簬闀挎湡璁板繂锛屼腑闂撮渶瑕?reflection銆?

鍦?`Niko` 閲岋細

- daily logs 绫讳技缁忛獙杈撳叆娴併€?
- Dream 鏄?reflection pass銆?
- `MEMORY.md` 鍜?topic files 鏄暣鐞嗗悗鐨勯暱鏈熻蹇嗐€?
- ContextManager 鍦ㄦ湭鏉?session 鎶婂叆鍙ｇ储寮曞甫鍥?prompt銆?

涔熷氨鏄锛宍Niko` 瀹炵幇鐨勬槸浠ｇ爜 agent 鍦烘櫙涓嬬殑涓€灏忓潡鍙嶆€濇満鍒讹紝涓嶆槸瀹屾暣鐨勭敓鎴愬紡瑙掕壊鏋舵瀯銆?

### MemGPT锛氫笂涓嬫枃绐楀彛澶栬鏈夊眰绾ц蹇?

MemGPT 浠庢搷浣滅郴缁熺殑灞傜骇鍐呭瓨寰楀埌鍚彂锛屾妸鏈夐檺 context window 澶栫殑闀夸笂涓嬫枃绠＄悊鎴愪笉鍚?memory tiers銆?

`Niko` 鐨勫疄鐜版洿绠€鍗曪紝娌℃湁铏氭嫙鍐呭瓨寮?paging锛屼篃娌℃湁 interrupt-based control flow銆備絾瀹冭В鍐崇殑鏄悓涓€绫诲帇鍔涳細context window 鏈夐檺锛屼笉鑳芥妸鎵€鏈夊巻鍙查兘鏀捐繘鍘汇€?

`Niko` 鐨勫仛娉曟槸鏄惧紡鏂囦欢灞傜骇锛?

- 鍚姩鍙姞杞?`MEMORY.md` 鐭储寮曘€?
- 璇︾粏 topic 鏂囦欢鎸夐渶璇诲彇銆?
- transcript 鍙仛绐勮寖鍥存悳绱€?
- Dream 瀹氭湡鎶婃棩蹇楀帇鎴?topic锛岃€屼笉鏄鏃ュ織鏃犻檺杩涘叆 prompt銆?

杩欎釜鏂规涓嶅 MemGPT 閫氱敤锛屼絾瀵规湰鍦?coding harness 鏇村鏄撹В閲娿€佽皟璇曞拰瀹℃煡銆?

---

## 褰撳墠瀹炵幇鐨勫叧閿彇鑸?

### 鍙栬垗涓€锛氭枃浠剁郴缁熶紭鍏堬紝涓嶅厛涓婃暟鎹簱

鏂囦欢绯荤粺鐨勫ソ澶勬槸閫忔槑銆?

鐢ㄦ埛鍙互鐩存帴鎵撳紑 `.niko/memory`锛岀湅鍒版ā鍨嬭浣忎簡浠€涔堬紝鍒犳帀閿欒鍐呭锛屾鏌?Dream 鏀逛簡鍝簺鏂囦欢銆傚涓€涓湰鍦?agent harness 鏉ヨ锛岃繖姣斾竴寮€濮嬪氨涓婃暟鎹簱鎴栧悜閲忓簱鏇村悎閫傘€?

浠ｄ环鏄煡璇㈣兘鍔涘急銆傛湭鏉ュ鏋?topic 鏂囦欢寰堝锛岄潬 `rg` 鍜屾ā鍨嬭绱㈠紩鍙兘涓嶅锛岄渶瑕佹洿濂界殑 metadata 鎴?embedding銆?

褰撳墠闃舵涓嶆€ョ潃涓婂悜閲忓簱銆傚厛鎶婄储寮曘€乼opic銆丏ream 缁存姢鍋氱ǔ锛屾瘮寮曞叆澶嶆潅妫€绱㈠眰鏇撮噸瑕併€?

### 鍙栬垗浜岋細Dream 澶嶇敤 Niko runtime锛屼笉鍐欑嫭绔?worker

澶嶇敤 Niko runtime 璁╁疄鐜板緢灏忥細

- 澶嶇敤 model client銆?
- 澶嶇敤 tool executor銆?
- 澶嶇敤 permission checker銆?
- 澶嶇敤 trace/session event銆?
- 澶嶇敤 workspace path 瑙ｆ瀽銆?

浠ｄ环鏄?Dream 瀛?agent 浠嶇劧甯︾潃涓€涓畬鏁?runtime 鐨勫鏉傚害銆傚畠闇€瑕侀€氳繃 feature flags 鍜?tool profile 琚富鍔ㄦ敹绐勶紝鍚﹀垯灏变細鍙樻垚鍙︿竴涓櫘閫?Niko銆?

褰撳墠瀹炵幇宸茬粡鍋氫簡鍏抽敭鏀剁獎锛氬叧闂?memory/relevant_memory锛岃缃?`dream` profile锛岃缃?`write_scope`锛屽叧闂?auto dream銆?

### 鍙栬垗涓夛細鍚庡彴绾跨▼鑰屼笉鏄閮?scheduler

鍚庡彴绾跨▼寰堣交锛岄€傚悎 CLI銆傜敤鎴锋嬁鍒?final 鍚庯紝Dream 缁х画鏁寸悊锛屼笉闇€瑕佸崟鐙畧鎶よ繘绋嬨€?

浠ｄ环鏄敓鍛藉懆鏈熻窡褰撳墠杩涚▼缁戝畾銆傚鏋?CLI 杩涚▼缁撴潫澶揩锛宒aemon thread 鍙兘杩樻病璺戝畬銆傚綋鍓嶅疄鐜版洿閫傚悎浜や簰寮?session锛岃€屼笉鏄弗鏍间繚璇佹瘡娆￠兘浼氬畬鎴愮殑绂荤嚎浣滀笟銆?

濡傛灉鏈潵瑕佷繚璇?Dream 涓€瀹氬畬鎴愶紝灏遍渶瑕佸閮?job runner 鎴栭潪 daemon thread 鐨勬樉寮忕瓑寰呯瓥鐣ャ€傜幇鍦ㄥ厛淇濇寔杞婚噺鏄悎鐞嗙殑銆?

### 鍙栬垗鍥涳細鍘熷湴淇敼 memory锛岃€屼笉鏄骇鍑哄€欓€?store

鍘熷湴淇敼鏈€绠€鍗曪紝涔熺鍚堟湰鍦版枃浠剁洿瑙夈€?

浣嗕粠鍙潬鎬х湅锛屼袱闃舵杈撳嚭鏇村ソ銆侻anaged Agents Dreams 閫夋嫨杈撳嚭鏂?store锛屽氨鏄负浜嗚杈撳叆 store 涓嶈鐩存帴鐮村潖锛岀敤鎴峰彲浠ュ鏌ュ悗鍒囨崲銆?

`Niko` 濡傛灉缁х画闈㈠悜闈㈣瘯鍜屾湰鍦?harness锛屽師鍦颁慨鏀瑰彲浠ユ帴鍙椼€傝寰€鏇存垚鐔熺殑浜у搧褰㈡€佽蛋锛屽氨搴旇鑰冭檻 `.dream-runs/<id>/output` 鎴?patch review 娴佺▼銆?

### 鍙栬垗浜旓細灏忔壒閲?session cap

`DREAM_SESSION_CAP = 30` 涓嶆槸闅忔剰鏁板瓧銆傚畠鍙嶆槧浜嗕竴涓幇瀹為棶棰橈細Dream 鐨勮緭鍏ヨ妯′笉鍙帶鏃讹紝寰堝鏄撹Е鍙?provider 涓婁笅鏂囨垨杈撳嚭寮傚父銆?

闀挎湡璁板繂鏁寸悊杩芥眰鐨勬槸绋冲畾澧為噺锛岃€屼笉鏄竴娆″悶瀹屽叏閮ㄥ巻鍙层€?

杩欏拰瀹樻柟 Dreams 鏂囨。閲岀殑鎴愭湰鎻愮ず涓€鑷达細鎴愭湰浼氶殢杈撳叆 sessions 鏁伴噺鍜岄暱搴﹀ぇ鑷村闀匡紝搴旇浠庡皬鎵归噺寮€濮嬨€?

---

## 澶辫触妯″紡鍜屽綋鍓嶉槻绾?

### 1. Dream 鍐欏嚭閲嶅 memory

鍘熷洜閫氬父鏄病鏈夊厛璇诲凡鏈?topic 鏂囦欢锛屾垨鑰?`MEMORY.md` 绱㈠紩涓嶆竻妤氥€?

褰撳墠闃茬嚎锛?

- prompt 鐨?Orient 闃舵瑕佹眰鍏堣 index 鍜?topic銆?
- Consolidate 闃舵瑕佹眰浼樺厛 merge锛岃€屼笉鏄垱寤鸿繎閲嶅鏂囦欢銆?
- Prune 闃舵瑕佹眰鍒犻櫎 stale/superseded 鎸囬拡銆?

杩樺彲浠ヨˉ锛?

- memory lint锛氭鏌ュ涓?topic 鏂囦欢鐨?`name`/`description` 鏄惁楂樺害鐩镐技銆?
- Dream report锛氬垪鍑烘湰娆′负浠€涔堟柊澧炴枃浠惰€屼笉鏄洿鏂版棫鏂囦欢銆?

### 2. Dream 淇濆瓨鐬椂浠诲姟鐘舵€?

鍘熷洜鏄ā鍨嬫妸褰撳墠 turn 鐨?next step銆乥locker銆乧ommand output 褰撴垚鏈潵涔熸湁鐢ㄧ殑淇℃伅銆?

褰撳墠闃茬嚎锛?

- `reject_durable_reason()` 杩囨护 checkpoint-like 鍓嶇紑銆?
- memory system section 鏄庣‘鍒楀嚭涓嶈淇濆瓨 transient task details銆乧urrent blockers銆乶ext steps銆?
- Dream prompt 鏄庣‘瑕佹眰涓嶈淇濆瓨 raw command output銆乻tack traces銆乼ransient task state銆?

杩樺彲浠ヨˉ锛?

- 瀵?Dream 鍐欏叆鐨?topic 鏂囦欢鍋氬悗缃鏌ワ紝鍑虹幇 `涓嬩竴姝銆乣褰撳墠鐩爣`銆乣stdout`銆乣traceback` 绛夎瘝鏃剁粰 warning銆?

### 3. Dream 淇濆瓨绉樺瘑

褰撳墠闃茬嚎锛?

- `SECRET_SHAPED_TEXT_PATTERN` 浼氳繃婊?`api key/token/secret/password` 鍜岀被浼?`sk-...` 鐨勫€笺€?
- prompt 鏄庣‘绂佹淇濆瓨 secrets銆乧redentials銆乼okens銆乸rivate keys銆?

杈圭晫锛?

- 姝ｅ垯鍙兘鎸′綇鏄庢樉 secret-shaped 鏂囨湰銆傛洿闅愯斀鐨勫嚟鎹牸寮忎粛鍙兘婕忚繃銆?

鍙互琛ワ細

- 鎺ュ叆椤圭洰宸叉湁 secret redaction 閫昏緫锛屽 Dream output 鍋氬悓鏍锋壂鎻忋€?
- 瀵?`.niko/memory` 鍐欏叆鍋氱粺涓€ pre-write guard锛岃€屼笉鍙槸鍦?promotion 闃舵杩囨护銆?

### 4. Dream 鍜屾墜鍔ㄧ紪杈戝啿绐?

鐢ㄦ埛鍙兘姝ｅ湪鎵嬪姩鏀?`.niko/memory`锛屽悗鍙?Dream 鍚屾椂 patch 鏂囦欢銆?

褰撳墠闃茬嚎杈冨急銆?

鍙互琛ワ細

- Dream 寮€濮嬪墠淇濆瓨 memory snapshot銆?
- 鍐欏叆鍓嶆鏌ユ枃浠?hash 鏄惁浠嶇瓑浜庡紑濮嬫椂璇诲彇鐨勭増鏈€?
- 濡傛灉涓嶄竴鑷达紝鍐欏叆鍊欓€?patch 鑰屼笉鏄洿鎺ヨ鐩栥€?

### 5. Provider 杩斿洖绌哄搷搴旀垨瓒呮椂

鍘熷洜鍙兘鏄?prompt 澶暱銆乻ession 澶銆佽緭鍑洪绠椾笉澶熴€佹ā鍨嬪悗绔笉绋冲畾銆?

褰撳墠闃茬嚎锛?

- `DREAM_SESSION_CAP = 30`銆?
- `DREAM_MIN_NEW_TOKENS = 4096`銆?
- 鑷姩 Dream 澶辫触鏃朵細鎶?lock mtime 鎭㈠鍒?previous mtime锛屽苟璁板綍 `memory_auto_dream_failed`銆?

杩樺彲浠ヨˉ锛?

- 杩炵画澶辫触璁℃暟鍜岄€€閬裤€?
- 澶辫触鍚庣缉灏?session batch锛屼緥濡?30 -> 10銆?
- 鍦?report 閲岃褰?input session 鏁板拰 prompt metadata锛屾柟渚垮畾浣嶆槸涓嶆槸涓婁笅鏂囪繃澶с€?

### 6. `.consolidate-lock` 鐘舵€佷笉鍑?

褰撳墠 lock 鏂囦欢鏃㈡槸閿佸張鏄?last consolidated timestamp銆傚疄鐜扮畝鍗曪紝浣嗙姸鎬佹贩鐢ㄣ€?

鍙互琛ワ細

- 淇濈暀 `.consolidate-lock` 鍋氶攣銆?
- 鏂板 `.last-consolidated.json` 淇濆瓨 last_success_at銆乻ession_ids銆乧hanged_files銆乪rror銆?

杩欐牱 gate 閫昏緫鍜屽苟鍙戦攣浼氭洿娓呮櫚锛岃皟璇曚篃鏇存柟渚裤€?

---

## 杩欎釜鍔熻兘闈㈣瘯閲屾€庝箞璁?

闈㈣瘯閲屼笉瑕佹妸 Dream 璁叉垚妯″瀷鑷姩鎬荤粨銆?

鏇村ソ鐨勮娉曟槸锛?

`Niko 鐨勯暱鏈熻蹇嗕笉鏄瘡杞兘鎶婂巻鍙插鍥?prompt锛岃€屾槸鍒嗘垚杈撳叆娴佸拰鏁寸悊缁撴灉銆?remember 鍜?<memory> 鍏堟妸鍊欓€変俊鎭啓杩?daily log锛孌ream 鍦?turn 缁撴潫鍚庢寜鏃堕棿鍜?session 鏁拌Е鍙戯紝鍚姩涓€涓彈闄愬瓙 agent 鍘昏 memory銆乴ogs 鍜屽繀瑕佺殑 transcripts锛屾妸绋冲畾淇″彿鍚堝苟杩?topic 鏂囦欢锛屽啀缁存姢 MEMORY.md 绱㈠紩銆傝繖鏍锋棦鑳借法 session 淇濆瓨鐢ㄦ埛鍋忓ソ鍜岄」鐩喅绛栵紝鍙堜笉浼氳 prompt 鏃犻檺澧為暱锛屼篃涓嶄細缁欏悗鍙颁换鍔″紑鏀句换鎰忓啓浠撳簱鐨勬潈闄愩€俙

杩介棶涓轰粈涔堜笉鐢ㄦ櫘閫?summary锛屽彲浠ヨ繖鏍疯锛?

`summary 涓昏鏄帇缂╀竴娈典笂涓嬫枃锛孌ream 缁存姢鐨勬槸涓€涓細琚湭鏉?session 鍙嶅浣跨敤鐨?memory store銆傚畠瑕佽В鍐抽噸澶嶃€佺煕鐩俱€佽繃鏈熷拰绱㈠紩鑶ㄨ儉锛屾墍浠ュ畠闇€瑕佽宸叉湁 memory銆佷慨鏀规棫鏂囦欢銆佸垹闄?stale entry锛岃€屼笉鏄彧浜у嚭涓€娈垫憳瑕併€俙

杩介棶涓轰粈涔堣鍗曠嫭瀛?agent锛屽彲浠ヨ繖鏍疯锛?

`涓?agent 鐨勮亴璐ｆ槸瀹屾垚鐢ㄦ埛浠诲姟锛孌ream 鐨勮亴璐ｆ槸缁存姢 memory銆傛媶鎴愬瓙 agent 鍚庡彲浠ョ嫭绔嬮檺鍒跺伐鍏烽泦鍜屽啓鍏ヨ寖鍥达紝澶辫触涔熷彧褰卞搷 memory maintenance锛屼笉褰卞搷杩欒疆鐢ㄦ埛浠诲姟銆侼iko 閲?dream profile 鍙厑璁歌宸ュ叿鍜?write/patch锛寃rite_scope 闄愬埗鍦?.niko/memory锛岃繖姣旈潬 prompt 绾︽潫瀹夊叏銆俙

杩介棶鍜?Claude Code/Managed Agents 鐨勫尯鍒紝鍙互杩欐牱璇达細

`鎴戝弬鑰冪殑鏄畠浠殑宸ョ▼褰㈡€侊紝涓嶆槸鐓ф妱 API銆侰laude Code autoDream 涔熸槸鍚庡彴鍙楅檺 agent 鍔?memory 鐩綍鍜?gate锛汳anaged Agents Dreams 鏇村儚浜戠寮傛璧勬簮锛屼細杈撳嚭鏂扮殑 memory store锛岃緭鍏?store 涓嶇洿鎺ヤ慨鏀广€侼iko 鐜板湪鏄湰鍦?CLI harness锛屾墍浠ラ€夋嫨鍘熷湴淇敼 .niko/memory锛屾崲鏉ョ畝鍗曢€忔槑銆傚悗缁鏋滆鏇翠骇鍝佸寲锛屽彲浠ヨˉ DreamTask 鐢熷懡鍛ㄦ湡鍜?output candidate store銆俙

---

## 鍚庣画鏀硅繘璺嚎

杩欓儴鍒嗘寜浼樺厛绾ф帓銆?

### P0锛氱粺涓€鎵嬪姩鍜岃嚜鍔?Dream 鐨勯攣

鎶?lock 閫昏緫涓嬫矇鍒?Dream 鎵ц鍏ュ彛锛屼繚璇?`/dream` 鍜?auto dream 涓嶄細骞跺彂鍐?memory銆?

楠屾敹鏍囧噯锛?

- 鑷姩 Dream 鎸侀攣鏃讹紝鎵嬪姩 `/dream` 杩斿洖鏄庣‘鎻愮ず銆?
- 鎵嬪姩 `/dream` 璺戝畬鍚庡悓鏍锋洿鏂?last consolidated timestamp銆?
- 娴嬭瘯瑕嗙洊 stale lock銆乴ock held銆乵anual run 涓夌鎯呭喌銆?

### P1锛氬鍔?memory lint

Dream 鍐欏畬鍚庤窇涓€涓‘瀹氭€ф鏌ワ細

- `MEMORY.md` 涓嶈秴杩?200 琛屻€?
- `MEMORY.md` entry 鎸囧悜鐨勬枃浠跺瓨鍦ㄣ€?
- topic 鏂囦欢 frontmatter 鍖呭惈 `name/description/type`銆?
- `type` 鍦ㄥ厑璁搁泦鍚堝唴銆?
- 鏂囦欢涓病鏈夋槑鏄?secret-shaped 鏂囨湰銆?
- 鏂囦欢涓病鏈夊父瑙?transient task state 鍓嶇紑銆?

楠屾敹鏍囧噯锛?

- lint warning 杩涘叆 run report銆?
- 涓ラ噸闂鍙互璁?Dream 鏍囪 failed 鎴?partial銆?

### P1锛欴ream report 缁撴瀯鍖?

褰撳墠 `last_dream_changed_files` 鑳藉憡璇夋敼浜嗗摢浜涙枃浠讹紝浣嗕笉鑳借В閲婁负浠€涔堟敼銆?

寤鸿璁?Dream 杈撳嚭缁撴瀯鍖?summary锛?

```json
{
  "updated": ["topics/user-preferences.md"],
  "created": [],
  "pruned": ["topics/old-debugging.md"],
  "sources": ["logs/2026/05/2026-05-13.md", "session:..."],
  "skipped": [
    {"reason": "transient_task_state", "text_preview": "..."}
  ]
}
```

楠屾敹鏍囧噯锛?

- report 鑳芥樉绀烘湰娆?Dream 鍋氫簡浠€涔堛€?
- 澶辫触鏃惰兘鐪嬪埌澶勭悊鍒板摢涓€姝ャ€?

### P2锛氬紩鍏?DreamTask 鐢熷懡鍛ㄦ湡

缁?Dream 涓€涓竴绛変换鍔″璞★紝鑷冲皯鍖呮嫭锛?

- id
- status
- session_ids
- started_at/ended_at
- changed_files
- error
- cancel/kill 鐘舵€?

杩欎細璁?TUI銆丆LI 鍜屾湭鏉?webhook/automation 閮芥洿濂芥帴銆?

楠屾敹鏍囧噯锛?

- `/dream` 鑳芥樉绀?running/completed/failed銆?
- auto dream 鐨勫悗鍙扮姸鎬佽兘琚煡璇€?
- 澶辫触涓嶄細鍙棌鍦?trace 閲屻€?

### P2锛氫袱闃舵杈撳嚭

鎶?Dream 鐨勫啓鍏ョ洰鏍囦粠鍘熷湴 memory 鐩綍鏀规垚 candidate output锛屽啀 apply銆?

杞婚噺鐗堟湰鍙互杩欐牱鍋氾細

```text
.niko/memory/.dream-runs/<run_id>/
鈹溾攢鈹€ input-snapshot.json
鈹溾攢鈹€ output/
鈹溾攢鈹€ report.json
鈹斺攢鈹€ patch.diff
```

楠屾敹鏍囧噯锛?

- 杈撳叆 memory 涓嶇洿鎺ヨ鐮村潖銆?
- 鐢ㄦ埛鍙互 review patch銆?
- apply 鍚庡啀鏇存柊 `.consolidate-lock`銆?

杩欎釜鏀瑰姩鏀剁泭澶э紝浣嗗鏉傚害涔熼珮锛屼笉閫傚悎浣滀负褰撳墠鏈€鍏堝仛鐨勪簨銆?

### P3锛氭洿缁嗙殑 session 閫夋嫨绛栫暐

褰撳墠鏄寜 mtime 鎵句笂娆?consolidation 涔嬪悗鐨?session锛屽啀鎴渶杩?30 涓€?

浠ュ悗鍙互鏀规垚锛?

- 浼樺厛鍖呭惈鏈?memory_note_appended銆乨urable promotion銆佺敤鎴锋槑纭?correction 鐨?session銆?
- 璺宠繃绾煭闂瓟鎴栨棤宸ュ叿璋冪敤 session銆?
- 澶辫触鍚庤嚜鍔ㄧ缉灏?batch銆?

楠屾敹鏍囧噯锛?

- 鍚屾牱 token 棰勭畻涓嬶紝Dream 鍛戒腑鏇村鐪熷疄鍙繚瀛樹俊鍙枫€?
- 澶?session 鐩綍涓嬩笉浼氭瘡娆℃壂鎻忓叏閲忔枃浠躲€?

---

## 鏈€灏忛獙鏀舵竻鍗?

褰撳墠 Dream 鍔熻兘瑕佺畻绔欏緱浣忥紝鑷冲皯瑕佽鐩栬繖浜涙祴璇曞拰鐪熷疄璺緞銆?

### 鍗曞厓娴嬭瘯

1. `ensure_memory_dir()` 鑳藉垱寤?`MEMORY.md`銆乣logs/`銆乣topics/`銆?
2. `/remember` 鑳借拷鍔?daily log锛屽苟鍐?session event銆?
3. `<memory>` 鏍囩鑳借 final 鍚庡鐞嗘彁鍙栥€?
4. `reject_durable_reason()` 鑳芥尅浣?secret-shaped 鏂囨湰銆佷复鏃剁姸鎬佸拰闀挎棩蹇椼€?
5. `evaluate_auto_dream_gate()` 瀵?interval gate銆乻ession gate銆乻hould_run 涓夌鍒嗘敮杩斿洖姝ｇ‘銆?
6. `build_dream_prompt()` 鍦?session_ids 瓒呰繃 30 鏃舵埅鏂紝骞跺湪 prompt 閲岃鏄庛€?
7. Dream 瀛?runtime 鐨?tool profile 涓嶅厑璁?run_shell銆乤gent銆乤sk_user銆?
8. write_scope 鑳芥尅浣?memory 鐩綍澶栧啓鍏ャ€?
9. auto Dream 澶辫触鏃?lock mtime 鑳藉洖婊氥€?
10. auto Dream 鎴愬姛鍚庤兘璁板綍 changed_files 鍜?`dream_consolidated` event銆?

### 鐪熷疄 CLI 楠屾敹

鏈€灏忕湡瀹為摼璺彲浠ヨ繖鏍疯窇锛?

涓嬮潰鍛戒护鍋囪椤圭洰 `.env`銆乣.niko.toml` 鎴栧叏灞€閰嶇疆閲屽凡缁忔湁鍙敤 provider銆俙/remember` 鍜?`/memory` 涓昏楠岃瘉鏈湴鍐欏叆涓庤鍙栵紝`/dream` 浼氱湡姝ｈ皟鐢ㄦā鍨嬨€?

```bash
uv run niko "/remember Preference: Niko docs should be written in direct Chinese."
uv run niko "/memory"
uv run niko "/dream"
find .niko/memory -maxdepth 3 -type f | sort
```

濡傛灉鐢ㄧ湡瀹炴ā鍨嬮獙鏀讹紝閲嶇偣鐪嬩笁浠朵簨锛?

1. `.niko/memory/logs/` 鏄惁鏈夊師濮?note銆?
2. Dream 鏄惁鍒涘缓鎴栨洿鏂?topic 鏂囦欢銆?
3. `MEMORY.md` 鏄惁鍙繚鐣欑煭绱㈠紩锛岃€屼笉鏄妸瀹屾暣璁板繂姝ｆ枃濉炶繘鍘汇€?

### 鍥炲綊椋庨櫓楠屾敹

鏀?Dream 鏃惰繕瑕佹鏌ヨ繖浜涜涓轰笉鑳藉潖锛?

- 鏅€氱敤鎴蜂换鍔?final 涓嶅簲璇ョ瓑寰?auto Dream 瀹屾垚銆?
- `--no-auto-dream` 蹇呴』瀹屽叏璺宠繃鑷姩 Dream銆?
- `--dream-interval` 鍜?`--dream-min-sessions` 蹇呴』褰卞搷 gate銆?
- 瀛?Dream 涓嶈兘瑙﹀彂鍙︿竴涓?auto Dream銆?
- Dream 澶辫触涓嶈兘鎶婁富浠诲姟鏍囪涓哄け璐ャ€?

---

## 鍙傝€冩潗鏂?

鏈璁′富瑕佸弬鑰冭繖浜涙潗鏂欙細

- 褰撳墠 `Niko` 浠ｇ爜锛歚niko_agent/features/memory.py`銆乣niko_agent/core/runtime.py`銆乣niko_agent/core/tool_profiles.py`銆乣niko_agent/core/permissions.py`銆乣niko_agent/core/context_manager.py`銆乣niko_agent/core/engine.py`銆乣niko_agent/cli.py`銆?
- 鏈湴 Claude Code 鐮旂┒鏉愭枡锛歚/Users/martinlos/code/civil-engineering-cloud-claude-code-source-v2.1.88/02-claude-code-source-research`銆傝繖浠芥潗鏂欑敤浜庣悊瑙?`memdir`銆乣extractMemories`銆乣autoDream`銆乣DreamTask` 绛夎璁″舰鎬侊紝闈㈣瘯閲屽簲鎸夌ぞ鍖烘仮澶?鐮旂┒鏉愭枡琛ㄨ堪銆?
- Anthropic Managed Agents Dreams 鏂囨。锛歚https://platform.claude.com/docs/en/managed-agents/dreams`銆?
- Claude Code memory 鏂囨。锛歚https://code.claude.com/docs/en/memory`銆?
- ReAct: Synergizing Reasoning and Acting in Language Models锛歚https://arxiv.org/abs/2210.03629`銆?
- Generative Agents: Interactive Simulacra of Human Behavior锛歚https://arxiv.org/abs/2304.03442`銆?
- MemGPT: Towards LLMs as Operating Systems锛歚https://arxiv.org/abs/2310.08560`銆?

---

## 鏈€鍚庢妸涓€鍙ヨ瘽鏀跺洖鏉?

`Niko` 鐨?Dream 鍔熻兘鍙互杩欐牱瀹氫綅锛?

**瀹冩槸鏈湴 coding agent 鐨勫悗鍙拌蹇嗙淮鎶ゅ眰锛岀敤鍙楅檺瀛愯繍琛屾椂鎶婅法 session 鐨勯浂鏁ｄ俊鍙锋暣鐞嗘垚鍙储寮曘€佸彲淇銆佷綆鍣０鐨勯暱鏈熻蹇嗐€?*

杩欎釜瀹氫綅姣旀ā鍨嬭嚜鍔ㄦ€荤粨鏇村噯纭紝涔熸洿鑳借В閲婁负浠€涔堜唬鐮侀噷浼氭湁 memory directory銆乨aily logs銆乼opic files銆乪ntrypoint index銆乤uto gate銆乴ock銆乨ream profile銆亀rite_scope 鍜屽悗鍙扮嚎绋嬨€?

褰撳墠瀹炵幇宸茬粡鎶婅繖鏉′富绾胯窇閫氥€傚悗闈㈡渶鍊煎緱琛ョ殑涓嶆槸鏇村 prompt锛岃€屾槸鏇寸‖鐨勪换鍔＄敓鍛藉懆鏈熴€佹洿濂界殑骞跺彂鎺у埗銆佺粨鏋勫寲 report銆乵emory lint锛屼互鍙婂湪闇€瑕佹椂寮曞叆鍊欓€?output store銆?

