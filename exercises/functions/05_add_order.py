"""
題目：寫一個新增訂單的函式，把新訂單加進訂單 list
練習概念：函式修改傳進來的 list（用 append 把資料加進去）
為什麼要學：你的 API 第 1 階段的「新增訂單」，不只是算出一筆訂單交回去，
           還要真的把它「存起來」，之後用 find_order 才查得到。

情境：小店有一個訂單 list，每次有客人下單，就要開一筆新訂單放進去。
      新訂單的格式照輔助材料 05_add_order.md 裡的表格（DBML）。
要求：定義一個函式 add_order(orders, item)：
        1. 照表格組出一筆新訂單 dict：
             "id"     → 目前訂單數量 + 1（現在有 3 筆，新的就是 4；一筆都沒有，新的就是 1）
             "item"   → 傳進來的商品名稱
             "status" → 固定是 "待付款"（新訂單一定還沒付錢）
        2. 用 append 把這筆訂單加進 orders 的最後面
        3. return 這筆新訂單
      提示：目前訂單數量可以用 len(orders) 取得。

Feature: 新增訂單

  Scenario: 已有 3 筆訂單，新增一筆
    Given 一個已經有 3 筆訂單的 list
    When 新增一筆「馬卡龍」訂單
    Then 拿回 {"id": 4, "item": "馬卡龍", "status": "待付款"}
    And  list 變成 4 筆，最後一筆就是剛新增的訂單

  Scenario: 一筆訂單都沒有（邊界條件），新增第一筆
    Given 一個空的 list []
    When 新增一筆「咖啡」訂單
    Then 拿回 {"id": 1, "item": "咖啡", "status": "待付款"}
    And  list 變成 1 筆

  Scenario: 連續新增兩筆，編號要接下去
    Given 一個空的 list []
    When 先新增「咖啡」，再新增「蛋糕」
    Then 第二筆的 id 是 2
"""

# === 你的答案（從這裡開始寫）===
def add_order(orders, item): #定義一個函式，新增訂單，名字叫 add_order，接收兩個參數 orders（訂單列表）、item（商品名稱），回傳一個 dict，表示那一筆訂單
  new_order = { #新訂單的格式照輔助材料 05_add_order.md 裡的表格（DBML）：
    "id": len(orders) + 1, #目前訂單數量 + 1（現在有 3 筆，新的就是 4；一筆都沒有，新的就是 1），用 len(orders) 取得
    "item": item, #商品名稱
    "status": "待付款", #固定是 "待付款"（新訂單一定還沒付錢）
  } #回傳一個 dict，表示那一筆訂單
  orders.append(new_order) #用 append 把這筆訂單加進 orders 的最後面，append 是 Python 的 list 方法，用來把新元素加到 list 的末尾
  return new_order #回傳這筆新訂單
# === 答案結束 ===

# === 驗收（不用改）===
# Scenario: 已有 3 筆訂單，新增一筆
orders = [
    {"id": 1, "item": "咖啡", "status": "待付款"},
    {"id": 2, "item": "蛋糕", "status": "已付款"},
    {"id": 3, "item": "禮盒", "status": "已出貨"},
]
new_order = add_order(orders, "馬卡龍")
assert new_order == {"id": 4, "item": "馬卡龍", "status": "待付款"}
assert len(orders) == 4
assert orders[-1] == {"id": 4, "item": "馬卡龍", "status": "待付款"}
# Scenario: 一筆訂單都沒有（邊界條件），新增第一筆
empty_orders = []
assert add_order(empty_orders, "咖啡") == {"id": 1, "item": "咖啡", "status": "待付款"}
assert len(empty_orders) == 1
# Scenario: 連續新增兩筆，編號要接下去
shop_orders = []
add_order(shop_orders, "咖啡")
assert add_order(shop_orders, "蛋糕")["id"] == 2
print("✅ 全部通過")
