"""
題目：寫一個查訂單的函式，用編號從一堆訂單裡找出那一筆
練習概念：在函式裡用迴圈找資料，找到就立刻 return
為什麼要學：你的 API 第 1 階段除了「新增訂單」，還要有「查訂單」：
           呼叫的人給你一個訂單編號，你從所有訂單裡找出那一筆交回去；找不到也要有明確的回應。

情境：小店的訂單都存在一個 list 裡（下方「已提供」區的 orders），每筆訂單是一個 dict，有 "id"、"item"、"status"。
要求：定義一個函式 find_order(orders, order_id)：
        - 逐筆檢查 orders，找到 "id" 等於 order_id 的那筆，就把「整筆訂單 dict」return 回去
        - 全部檢查完都沒找到，就 return None
      None 是 Python 表示「什麼都沒有」的值，就像查詢結果寫著「查無此筆」。
輔助材料：同資料夾的 04_find_order.md，畫出迴圈一筆一筆檢查的流程。

Feature: 用編號查訂單

  Scenario: 編號存在，回傳那一筆訂單
    Given 已提供的 orders 裡有編號 2 的訂單（蛋糕）
    When 查編號 2
    Then 拿回 {"id": 2, "item": "蛋糕", "status": "已付款"}

  Scenario: 編號不存在（邊界條件），回傳 None
    Given 已提供的 orders 裡沒有編號 99
    When 查編號 99
    Then 拿回 None

  Scenario: 一筆訂單都沒有（邊界條件），回傳 None
    Given 一個空的 list []
    When 查編號 1
    Then 拿回 None
"""

# === 已提供（不用改）===
orders = [
    {"id": 1, "item": "咖啡", "status": "待付款"},
    {"id": 2, "item": "蛋糕", "status": "已付款"},
    {"id": 3, "item": "禮盒", "status": "已出貨"},
]


# === 你的答案（從這裡開始寫）===


# === 答案結束 ===

# === 驗收（不用改）===
# Scenario: 編號存在，回傳那一筆訂單
assert find_order(orders, 2) == {"id": 2, "item": "蛋糕", "status": "已付款"}
assert find_order(orders, 3)["item"] == "禮盒"
# Scenario: 編號不存在（邊界條件），回傳 None
assert find_order(orders, 99) is None
# Scenario: 一筆訂單都沒有（邊界條件），回傳 None
assert find_order([], 1) is None
print("✅ 全部通過")
