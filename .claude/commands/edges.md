---
description: 三明治底層：報告邊界條件、資料流與測試是否被動過
argument-hint: [專案資料夾名稱（可省略）]
---

為專案產出底層審查報告。專案：$ARGUMENTS

1. 確定專案：有指定就用指定的；否則用這次對話中正在進行的專案。讀它的 `SPEC.md`、`features/`、`schema.dbml`、測試與實作。
2. 執行 `uv run pytest projects/<專案>`，記錄每個 Scenario 的 green／red。
3. 檢查 `.feature` 與測試檔自學習者確認的那次 commit 之後有沒有被改過（`git log` 找出該 commit，再 `git diff <commit> -- projects/<專案>/features projects/<專案>/tests`）。有改動就逐一列出並說明理由；`.feature` 的改動要特別標示，因為那是學習者寫的契約。
4. 用白話寫報告，四段：
   - **資料流**：輸入 → 經過哪些步驟 → 輸出，每步一行。
   - **已處理的邊界條件**：以 Scenario 為單位，每一條寫「Scenario 名稱 → 程式怎麼應對」。
   - **未處理的邊界條件**：`.feature` 沒涵蓋的情況，每一條寫「如果 X 發生，會怎樣」，並建議要不要補成新的 Scenario。
   - **測試狀態**：各 Scenario 的 green／red，以及 `.feature`／測試檔是否被動過。
5. 請學習者親自執行成品一次，對照 `.feature` 的驗收條件。

完成條件：四段都有內容，`.feature` 中每一個 Scenario 都列在「已處理」並標明 green／red。
