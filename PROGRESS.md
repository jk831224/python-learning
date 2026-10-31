# 學習進度

由 `/wrap` 更新；學習者也可隨時手動修改。

## 1. 目前專案與路線

- 路線（2026-10-31 調整，學習者想透過「自己做 API、自己呼叫」實戰學 API）：
  (c) 迷你訂單 API 先做 → (a) Excel／CSV 自動化 → (b) 呼叫 Claude API 做文件摘要工具
- (c) 的分階段：
  1. ✅ 本機版 API：[projects/order_api/](projects/order_api/)，2026-10-31 完成（17 個 Scenario 全部 green、店員程式由學習者親手驗收）
  2. 網路版 API（B 階段）：用 FastAPI 把同一份契約放上 HTTP，店員網頁由 AI 撰寫（安裝套件前先問）
  3. 加訂單狀態規則（待付款 → 已付款 → 已出貨）與錯誤回應
- 目前專案：(c) 第 1 階段三明治三層都已走完；下一步是 B 階段的頂層（另開 SPEC）

## 2. 已掌握的語法

- 看得懂基礎語法（尚未逐項確認）
- 定義函式、參數、`return` 回傳值；分得出 `return` 與 `print` 的差別（functions/01）
- 函式回傳 dict，key 照約定一字不差（functions/02）
- 在函式裡呼叫其他函式（functions/03）
- 函式裡用 `for` + `if` 找資料，找到就 `return`，迴圈外 `return None`（functions/04）
- `len()` 與 `list.append()`，用變數存中間結果（functions/05）
- 字串的 `.strip()`：先去掉前後空白再比對（order_api 空白商品名稱修正；經第 3 級提示後看解答完成）

見過但尚未練習（Claude 寫的程式裡出現過，已有教材逐行解說，見 [notes/order-api-stage1-review.md](notes/order-api-stage1-review.md)）：`raise ValueError`、`input()`、`while True`、`try / except`、f-string、`import`、裝飾器、fixture、正規表示式、list comprehension

## 3. 四個概念的掌握程度

等級：沒碰過／見過／能解釋／能應用

| 概念 | 程度 | 備註 |
|---|---|---|
| 資料流 | 見過 | 03 串起三個函式；05 讓資料落腳在 list；order_api 審過循序圖、親手操作店員程式 → API 的流程 |
| 狀態機 | 沒碰過 | order_api 第 1 階段刻意略過；/edges 發現「查回的 dict 被改，存的訂單也跟著變」，留到第 3 階段 |
| API 契約 | 能應用（在選項引導下） | order_api 由學習者決定輸入輸出欄位、失敗方式（ValueError＋訊息）、錯誤訊息文字、檢查順序；理解「錯誤訊息也是契約」 |
| 邊界條件 | 能應用（在選項引導下） | 決定 0 合法、負數失敗、.5 進位、贈品照收運費、2.0 視為整數、空白名稱失敗；驗收時自己多測「兩個欄位同時錯」 |

## 4. 常犯的錯

- 縮排用 2 格而非 4 格（×4：02、03、04、05）→ 建議把 VS Code 右下角「Spaces」改成 4
- 函式定義結束後沒空兩行就接其他程式（×2 以上：01、02、03）
- 註解整段抄題目，讓單行變很長（×4：02、03、04、05）
- 同一個函式重複呼叫好幾次，沒用變數存中間結果（×1：03；05 已自己改用變數）
- 註解描述回傳值時漏寫例外情況（×1：04 漏寫「找不到回傳 None」）
- 寫完沒存檔就 `/check`（×1：01）
- 修 bug 時寫死特定值比對，只修好眼前的測試、弄壞原本通過的（×1：order_api 把 `item == ""` 改成 `item == "  "`）
- 實作時自行加入契約外的規則，違反自己定的 SPEC（×1：order_api 加了「單價不能是 0」，與「贈品單價 0 合法」衝突）→ 規則要改，先改 SPEC 與 `.feature`

## 待解鎖的練習類型

- 翻譯題：給一份 `.feature` 或 `.dbml`，寫出對應的 Python（或反向）。解鎖條件：能自己寫函式。→ **已達成（2026-10-31，functions/01–05）**，可開始出

## 5. 下次從哪裡接續

- 輸入 `/spec`，定義 (c) 的 B 階段：FastAPI 把 order_api 放上 HTTP ＋ AI 撰寫的店員網頁
- 開始前想複習，讀 `notes/`（2026-10-31 已寫好三份，開頭 YAML 標明脈絡）：
  - [functions-01-05-syntax-review.md](notes/functions-01-05-syntax-review.md)：函式練習用到的語法
  - [order-api-stage1-review.md](notes/order-api-stage1-review.md)：訂單 API 第 1 階段全貌、店員程式與測試程式碼逐行解說
  - [pytest-bdd-how-it-works.md](notes/pytest-bdd-how-it-works.md)：pytest／pytest-bdd 幕後運作
- 想要新的教材：`/note <主題>`
- 待處理：README「想達成的效果」的專案路線仍是舊順序，尚未更新
