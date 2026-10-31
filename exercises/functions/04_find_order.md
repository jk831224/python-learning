---
title: 04 輔助材料：一筆一筆找的流程
type: exercise-aid
exercise: exercises/functions/04_find_order.py
format: mermaid-flowchart
created: 2026-10-31
updated: 2026-10-31
concepts: [邊界條件]
topics: [for, if, return, None]
sources: [exercises/functions/04_find_order.py]
related: [notes/functions-01-05-syntax-review.md]
---

# 04 輔助材料：一筆一筆找的流程

以 `find_order(orders, 2)` 為例：先看第 1 筆（id 是 1，不是）→ 再看第 2 筆（id 是 2，是！）→ 立刻交回，第 3 筆不用看了。

```mermaid
flowchart TD
    A([呼叫 find_order]) --> B{還有下一筆訂單嗎？}
    B -- 有 --> C[拿出這一筆訂單]
    C --> D{這筆的 id 等於 order_id？}
    D -- 是 --> E([return 這筆訂單])
    D -- 不是 --> B
    B -- 沒有了 --> F([return None])
```

讀圖重點：

- 「是」的那條路一走到 `return`，函式就**立刻結束**，後面的訂單不會再檢查。
- `return None` 只有在**全部都看完**還沒找到時才會走到。想想看：這行該放在迴圈裡面，還是迴圈外面？
- 傳進空的 list `[]` 時，第一次問「還有下一筆嗎？」答案就是「沒有了」，直接走到 `return None`。
