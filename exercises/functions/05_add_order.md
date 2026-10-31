---
title: 05 輔助材料：一筆訂單長什麼樣子
type: exercise-aid
exercise: exercises/functions/05_add_order.py
format: dbml
created: 2026-10-31
updated: 2026-10-31
concepts: [資料流]
topics: [dict, list, DBML]
sources: [exercises/functions/05_add_order.py]
related: [notes/functions-01-05-syntax-review.md]
---

# 05 輔助材料：一筆訂單長什麼樣子

下面是用 DBML 寫的「訂單」表格定義。DBML 是描述資料表的格式，你可以把它想成 Excel 表頭：每一行是一個欄位，寫著欄位名稱、型別和說明。

```dbml
Table orders {
  id     int     [note: '訂單編號，從 1 開始往上加']
  item   varchar [note: '商品名稱']
  status varchar [note: '訂單狀態，新訂單一律是 待付款']
}
```

表格裡的資料（目前 3 筆）：

| id | item | status |
|---|---|---|
| 1 | 咖啡 | 待付款 |
| 2 | 蛋糕 | 已付款 |
| 3 | 禮盒 | 已出貨 |

## 從表格到 Python

表格的**一列** = Python 的**一個 dict**；欄位名稱變成 key，格子裡的值變成 value。
例如第 1 列寫成 Python 就是：

```python
{"id": 1, "item": "咖啡", "status": "待付款"}
```

**整張表** = 一個裝著好幾個 dict 的 **list**。

這題要你做的，就是在表格最下面「多加一列」：先照上面的格式組出那一列的 dict，再把它加進 list。
