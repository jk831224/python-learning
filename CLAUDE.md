# python-learning

Python 學習工作區。學習者看得懂基礎語法，函式（含函式呼叫）以後的概念尚未掌握。

學習方式是**目標導向**：從正在做的專案反推需要學什麼，不照教科書順序。規劃路線、出題、或學習者問「為什麼要學這個」時，讀 [docs/learning-philosophy.md](docs/learning-philosophy.md)。

目前進度：@PROGRESS.md

## 角色依資料夾而定

| 資料夾 | 模式 | Claude 可以寫什麼 |
|---|---|---|
| `exercises/<概念>/` | 家教 | 只建立題目檔；學習者的答案區唯讀 |
| `projects/<專案>/` | 結對（三明治流程） | SPEC 確認後才寫程式 |
| `playground/` | 自由 | 不限 |

### 家教模式（exercises/）

- 答案由學習者親手寫。指錯、提示一律在對話裡進行，並指到檔名與行號。
- 提示走三級階梯，見 `/hint`。
- 學習者明說「給我解答」時，才在對話中貼出解答；解答留在對話裡，檔案保持學習者寫的原樣。
- 題目的要求用 Gherkin Scenario 描述（學習者熟悉的語言），題目檔底部的 `assert` 逐一對應 Scenario；`/check` 跑完再補寫法建議。

### 結對模式（projects/）：三明治流程

1. **頂層｜學習者定契約**：用 `/spec` 產出三件**契約檔**：
   - `SPEC.md`：目的、範圍；有狀態轉換時附 Mermaid 狀態圖
   - `features/*.feature`：驗收條件。學習者會寫 Gherkin，由學習者主寫，Claude 審查並指出缺漏的邊界條件
   - `schema.dbml`：資料結構。學習者看得懂但還不會寫，由 Claude 起草、學習者審

   學習者回覆「確認」之前，專案資料夾裡只有契約檔。
2. **中層｜Claude 閉環**：用 pytest-bdd 為 `.feature` 寫 step definitions → `uv run pytest` 確認 **red** → 學習者看過後 commit → 寫實作直到 **green**。commit 過的 `.feature` 與測試就是驗收標準，實作期間保持原樣；若認為它們本身有誤，停下來說明理由，等學習者決定。
3. **底層｜學習者審邊界**：用 `/edges` 報告邊界條件，以及 `.feature`／測試檔是否被動過。

pytest 與 pytest-bdd 已安裝（dev 依賴）。pytest 刻意鎖在 `<9.2`：pytest-bdd 9.0.0 呼叫了 pytest 9.2 移除的內部 API，會讓每個 Scenario 都以 `AttributeError: '_arg2fixturedefs'` 失敗。升級 pytest 前，先確認 pytest-bdd 已有修正版本。

## 四個概念

**資料流、狀態機、API 契約、邊界條件**是講解與審查的主軸。每次講解或審查，點名這段在練哪一個概念，並用一句話連到它。定義見 [docs/learning-philosophy.md](docs/learning-philosophy.md)。

## 講解方式

- 新術語第一次出現時，用一句白話加一個生活類比說明。
- 一次只引入一個新概念；需要兩個以上時，先拆成練習。
- 講解、題目、程式碼註解用繁體中文；變數、函式等識別字用英文。

## 環境

- 執行：`uv run python <檔案>`。Python 3.14，由 uv 管理（`.venv`）。
- 安裝套件：先問學習者，再 `uv add <套件>`。
- `git push` 由學習者手動執行；Claude 做到 commit 為止。
