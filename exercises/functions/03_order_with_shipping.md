# 03 輔助材料：資料怎麼在函式之間傳

以「咖啡 80 元買 2 杯」為例。每個箭頭往右是「呼叫並把資料交過去」，虛線往左是「`return` 交回結果」。

```mermaid
sequenceDiagram
    participant 呼叫的人
    participant create_order
    participant calculate_total
    participant calculate_shipping

    呼叫的人->>create_order: create_order("咖啡", 80, 2)
    create_order->>calculate_total: calculate_total(80, 2)
    calculate_total-->>create_order: return 160
    create_order->>calculate_shipping: calculate_shipping(160)
    calculate_shipping-->>create_order: return 60
    Note over create_order: amount_due = 160 + 60
    create_order-->>呼叫的人: return {"item": "咖啡", ..., "amount_due": 220}
```

讀圖重點：

- `create_order` 自己不算金額、也不判斷運費，它只負責「問人」再把答案組起來。
- `calculate_shipping` 需要的 160，是從 `calculate_total` 拿回來的。上一個函式的輸出，變成下一個函式的輸入。
