# 學習進度

由 `/wrap` 更新；學習者也可隨時手動修改。

## 1. 目前專案與路線

- 路線（2026-10-31 調整，學習者想透過「自己做 API、自己呼叫」實戰學 API）：
  (c) 迷你訂單 API 先做 → (a) Excel／CSV 自動化 → (b) 呼叫 Claude API 做文件摘要工具
- (c) 的分階段：
  1. ✅ 本機版 API：[projects/order_api/](projects/order_api/)，2026-10-31 完成（17 個 Scenario 全部 green、店員程式由學習者親手驗收）
  2. ✅ 網路版 API（B 階段）：[projects/order_api_web/](projects/order_api_web/)，2026-11-02 完成。範圍擴大為 FastAPI ＋ SQLite 永久保存 ＋ 狀態機（待付款 → 已付款／已取消，已付款 → 已退款）＋ 店員網頁（Playwright 自動測試）。58 個 Scenario 全部 green；字體大小由學習者親手驗收
  3. 狀態規則的後續：出貨、送達、逾時自動取消（B 階段已先做付款與取消）
- 目前專案：(c) B 階段三明治三層都已走完，含一輪 `/edges` → 補契約 → red → green
  - 這次 Gherkin 由 Claude 起草、學習者審（學習者主動要求）；程式全部由 Claude 撰寫
  - 尚未決定：第 1 階段 [order_api.py](projects/order_api/order_api.py) 先檢查商品名稱，與它自己的 SPEC 順序不一致（測試沒抓到）

## 2. 已掌握的語法

- 看得懂基礎語法（尚未逐項確認）
- 定義函式、參數、`return` 回傳值；分得出 `return` 與 `print` 的差別（functions/01）
- 函式回傳 dict，key 照約定一字不差（functions/02）
- 在函式裡呼叫其他函式（functions/03）
- 函式裡用 `for` + `if` 找資料，找到就 `return`，迴圈外 `return None`（functions/04）
- `len()` 與 `list.append()`，用變數存中間結果（functions/05）
- 字串的 `.strip()`：先去掉前後空白再比對（order_api 空白商品名稱修正；經第 3 級提示後看解答完成）

見過但尚未練習（Claude 寫的程式裡出現過，已有教材逐行解說，見 [notes/order-api-stage1-review.md](notes/order-api-stage1-review.md)）：`raise ValueError`、`input()`、`while True`、`try / except`、f-string、`import`、裝飾器、fixture、正規表示式、list comprehension

見過但尚未練習、**還沒有教材**（B 階段 Claude 寫的程式，2026-11-02）：FastAPI 端點裝飾器（`@app.post`）、`HTTPException`、pydantic `BaseModel`、dict 當查表用（`TRANSITIONS.get(...)`）、`sqlite3` 與四句 SQL（`CREATE TABLE`／`INSERT`／`SELECT`／`UPDATE`）、HTML＋JavaScript（`fetch`）、Playwright 的 `expect`

本次沒有親手寫程式，語法清單無新增。

## 3. 四個概念的掌握程度

等級：沒碰過／見過／能解釋／能應用

| 概念 | 程度 | 備註 |
|---|---|---|
| 資料流 | 能解釋（在選項引導下） | 03 串起三個函式；05 讓資料落腳在 list；order_api 審過循序圖、親手操作店員程式 → API 的流程。B 階段：選「網頁和 API 都檢查」並理解理由（有人會繞過網頁）；自己指出「資料只在記憶體裡很可惜」，主動要求永久保存 |
| 狀態機 | 能解釋 | B 階段：自己提出規則「已取消不能付款、已付款取消要退款」；選擇另立 `已退款` 狀態；審過轉換表（都不能回頭、兩個終點）。尚未自己寫出狀態機程式，也還沒自己列出 ❌ 的 Scenario |
| API 契約 | 能應用（在選項引導下） | order_api 由學習者決定輸入輸出欄位、失敗方式（ValueError＋訊息）、錯誤訊息文字、檢查順序；理解「錯誤訊息也是契約」。B 階段：選定 201／400／404／409／422、端點網址、欄位一個都不改；收回「權限」需求以免失焦 |
| 邊界條件 | 能應用（在選項引導下） | 決定 0 合法、負數失敗、.5 進位、贈品照收運費、2.0 視為整數、空白名稱失敗；驗收時自己多測「兩個欄位同時錯」。B 階段：/edges 後定下數量上限 99、單價上限 99999，選「上限用原本的值判斷」以和負數規則一致 |

## 4. 常犯的錯

- 縮排用 2 格而非 4 格（×4：02、03、04、05）→ 建議把 VS Code 右下角「Spaces」改成 4
- 函式定義結束後沒空兩行就接其他程式（×2 以上：01、02、03）
- 註解整段抄題目，讓單行變很長（×4：02、03、04、05）
- 同一個函式重複呼叫好幾次，沒用變數存中間結果（×1：03；05 已自己改用變數）
- 註解描述回傳值時漏寫例外情況（×1：04 漏寫「找不到回傳 None」）
- 寫完沒存檔就 `/check`（×1：01）
- 修 bug 時寫死特定值比對，只修好眼前的測試、弄壞原本通過的（×1：order_api 把 `item == ""` 改成 `item == "  "`）
- 實作時自行加入契約外的規則，違反自己定的 SPEC（×1：order_api 加了「單價不能是 0」，與「贈品單價 0 合法」衝突）→ 規則要改，先改 SPEC 與 `.feature`
- （2026-11-02 B 階段沒有親手寫程式，無新增）

## 待解鎖的練習類型

- 翻譯題：給一份 `.feature` 或 `.dbml`，寫出對應的 Python（或反向）。解鎖條件：能自己寫函式。→ **已達成（2026-10-31，functions/01–05）**，可開始出

## 5. 下次從哪裡接續

- 建議先輸入 `/next`：B 階段的程式都是 Claude 寫的，用一題**翻譯題**把狀態機變成自己的——給 SPEC 的狀態轉換表，親手寫出「目前狀態＋動作 → 下一個狀態，不能走就回錯誤訊息」的函式
- 想先看懂 B 階段的程式：`/note B 階段`（FastAPI、SQL、網頁 JavaScript 逐行解說，目前還沒有這份教材）
- 之後的路線二選一：(c) 第 3 階段（出貨、送達、逾時自動取消），或進入 (a) Excel／CSV 自動化
- 開始前想複習，讀 `notes/`（2026-10-31 已寫好三份，開頭 YAML 標明脈絡）：
  - [functions-01-05-syntax-review.md](notes/functions-01-05-syntax-review.md)：函式練習用到的語法
  - [order-api-stage1-review.md](notes/order-api-stage1-review.md)：訂單 API 第 1 階段全貌、店員程式與測試程式碼逐行解說
  - [pytest-bdd-how-it-works.md](notes/pytest-bdd-how-it-works.md)：pytest／pytest-bdd 幕後運作
- 想要新的教材：`/note <主題>`
- 待處理：
  - README「想達成的效果」的專案路線仍是舊順序，尚未更新
  - 第 1 階段檢查順序不一致：要修就先補 Scenario（商品空白＋數量錯）
  - 測試出現 `StarletteDeprecationWarning`，建議改用 `httpx2`；換套件前先問學習者
