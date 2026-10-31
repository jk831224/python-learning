# python-learning

一套用 **VS Code + Claude Code** 學 Python 的工作區。重點不是讓 AI 代寫程式，而是把 AI 設定成「家教」與「結對夥伴」兩種角色，並用 PM 熟悉的規格語言（Gherkin、DBML）當作通往程式碼的橋梁。

## 為什麼做這個

我是 PM 出身，看得懂基礎的 Python 語法，但函式、函式呼叫之後就不懂了。工作上常要跟工程師與 AI agent 協作，我發現自己的問題是**知道這些技術有價值，卻不知道背後的原理**。

直接叫 AI 寫程式很快，但我學不到東西；照教科書從第一章讀起，又很快就失去動力。我需要一個能讓我「自己動手、但不會卡死」的環境。

## 學習觀念：來自一位資深工程師的建議

設計這套工作區之前，一位資深工程師朋友給了我幾個建議，成為整個設計的骨架（完整整理見 [docs/learning-philosophy.md](docs/learning-philosophy.md)）：

1. **目標導向**：不知道自己要做什麼，看教材只會想睡。先找到想做出的東西，再反推需要學什麼。選擇比努力重要。
2. **四個概念比語法更重要**：
   - **資料流**：資料從哪進來、經過哪幾層、最後落在哪
   - **狀態機**：狀態之間怎麼轉換、能不能回頭（例：付款到一半斷線，能重付還是要重新下單？）
   - **API 契約**：雙方約定交換什麼格式、哪些欄位
   - **邊界條件**：怎樣算合法、怎樣算壞掉、壞掉時怎麼應對
3. **三明治協作流程**：跟 AI agent 協作時，不要直接說「幫我做一個購物車」。
   - 頂層由**人**定契約（資料結構＋驗收條件）
   - 中層由 **agent** 閉環（先寫測試、確認失敗、再實作到通過，不准改測試）
   - 底層由**人**審邊界（要 agent 說明處理了哪些邊界條件）

## 想達成的效果

- 會讀、會寫基礎 Python，而且每學一樣東西都知道它是為了什麼
- 能用這四個概念看懂一個系統，跟工程師溝通時講得到點上
- 學會用三明治流程跟 AI agent 協作：自己定契約、讓 agent 實作、自己驗收
- 沿著一條專案路線，把五個目標（自動化、資料分析、後端、AI 應用、看懂程式碼）串起來：
  1. Excel／CSV 自動化與資料處理
  2. 呼叫 Claude API 的文件摘要工具
  3. 迷你訂單 API 與狀態機

## 設計

### 資料夾決定 Claude 的角色

| 資料夾 | 模式 | Claude 能做什麼 |
|---|---|---|
| `exercises/<概念>/` | 家教 | 只出題、給提示、批改；答案由我親手寫 |
| `projects/<專案>/` | 結對（三明治流程） | 契約確認後才寫程式 |
| `playground/` | 自由 | 不限 |
| `notes/` | 教材 | 我要求時，寫複習或延伸閱讀的文件 |

`notes/` 放「只讀不練」的教材。我不背語法，平常是讓 AI 補完程式碼再理解意思，所以教材的目標是**看到程式碼能翻成一句中文**：逐行白話翻譯，範例取自我做過的題目。例如 [functions-01-05-syntax-review.md](notes/functions-01-05-syntax-review.md) 整理了函式練習 01–05 用到的語法。

家教模式是這套方法的核心：Claude **不能改我寫的答案**，提示分三級（方向 → 概念 → 類比範例），只有我明說「給我解答」時才會給。

### 用已知的語言學新的語言

我以前當 PM 會寫 Gherkin 格式的 user story，也看得懂 UML 和 DBML。所以題目與專案規格刻意用這些格式來寫：

- **練習題**：要求寫成 Gherkin Scenario，每個 Scenario 對應題目檔底部的一組 `assert`。我等於在練「把熟悉的驗收語言翻譯成 Python」。
- **輔助材料**：練流程時附 Mermaid 圖，練資料結構時附 DBML。
- **專案契約**：`SPEC.md`＋`features/*.feature`＋`schema.dbml`。`.feature` 由我主寫，透過 [pytest-bdd](https://github.com/pytest-dev/pytest-bdd) 直接變成可執行的測試。

### Slash commands

| 指令 | 用途 |
|---|---|
| `/next` | 依目前專案的需要，出下一題練習 |
| `/hint` | 給下一級提示，不給答案 |
| `/check` | 執行題目檔，依 Scenario 回報對錯，再給寫法建議 |
| `/wrap` | 結束這次學習：更新進度檔並 commit |
| `/spec` | 三明治頂層：用提問帶我寫出專案契約 |
| `/edges` | 三明治底層：報告邊界條件、資料流，以及測試有沒有被偷改 |

指令內容在 [.claude/commands/](.claude/commands/)。

### 跨對話的記憶

[PROGRESS.md](PROGRESS.md) 記錄目前專案、已掌握的語法、四個概念的掌握程度、常犯的錯、下次從哪裡接續。[CLAUDE.md](CLAUDE.md) 會自動把它載入每次對話，所以開新對話時 Claude 知道我學到哪。

### 護欄

- `.claude/settings.json`：Claude 可以自己執行程式與 commit；安裝套件要先問我；`git push` 與 `rm -rf` 一律禁止
- 專案的測試確認後先 commit，之後若被改動，`git diff` 一定看得到，`/edges` 也會主動回報

## 一次學習的樣子

```
/next        → Claude 說明這題為什麼要學，在 exercises/ 建立題目檔
（自己寫）    → uv run python exercises/functions/01_xxx.py
/hint        → 卡住時拿提示
/check       → 批改，看哪個 Scenario 沒過
/wrap        → 更新 PROGRESS.md 並 commit
git push     → 自己推上 GitHub
```

## 想用這套方法？

需要的工具：

- [uv](https://docs.astral.sh/uv/)：管理 Python 版本與套件
- [Claude Code](https://claude.com/claude-code)
- VS Code，以及 Microsoft 官方的 Python 擴充套件

```bash
git clone https://github.com/jk831224/python-learning.git
cd python-learning
uv sync
claude
```

改成你自己的版本時，建議先修改這三處：

1. [CLAUDE.md](CLAUDE.md) 開頭的學習者描述（你的程度）
2. [PROGRESS.md](PROGRESS.md) 的專案路線（你想做出什麼）
3. 刪掉 `exercises/` 裡我的練習紀錄與 `notes/` 裡我的教材

如果你熟悉的不是 Gherkin，也可以把 `/next` 和 `/spec` 裡的格式換成你已經會的語言。這套方法的關鍵是「從已知走向未知」，格式本身不是重點。

## 備註

- Python 3.14，由 uv 管理。
- pytest 鎖在 `<9.2`：pytest-bdd 9.0.0 呼叫了 pytest 9.2 移除的內部 API，會讓每個 Scenario 都失敗。
- 這套工作區是我跟 Claude 一問一答釐清需求後建立的，目前仍在學習中，設計會繼續調整。
