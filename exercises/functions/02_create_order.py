"""
題目：寫一個建立訂單的函式，把整筆訂單打包成 dict 回傳
練習概念：函式回傳 dict（一次交回好幾個欄位）
為什麼要學：你的 API 第 1 階段要做「新增訂單」，呼叫的人會拿回一整筆訂單，
           而不是單一個數字。用 dict 把欄位打包起來，就是在約定「訂單長什麼樣子」。

情境：小店收到一筆訂單，要把它記錄下來，包含商品名稱、單價、數量和總金額。
要求：定義一個函式，名字叫 create_order，接收三個參數 item（商品名稱）、price（單價）、quantity（數量），
      回傳一個 dict，裡面要有四個欄位（key 的名字要一模一樣）：
        "item"     → 商品名稱
        "price"    → 單價
        "quantity" → 數量
        "total"    → 總金額（單價 × 數量）
範例：create_order("咖啡", 80, 2) → {"item": "咖啡", "price": 80, "quantity": 2, "total": 160}
"""

# === 你的答案（從這裡開始寫）===
def create_order(item, price, quantity): #定義一個函式，名字叫 create_order，接收三個參數 item（商品名稱）、price（單價）、quantity（數量），回傳一個 dict，裡面要有四個欄位（key 的名字要一模一樣）：
  return { #回傳一個 dict，裡面要有四個欄位（key 的名字要一模一樣）：
    "item": item, #商品名稱
    "price": price, #單價
    "quantity": quantity, #數量
    "total": price * quantity #總金額（單價 × 數量）
  }
print(create_order("咖啡", 80, 2)) #範例：create_order("咖啡", 80, 2) → {"item": "咖啡", "price": 80, "quantity": 2, "total": 160}

# === 答案結束 ===

# === 驗收（不用改）===
# 一般情況
assert create_order("咖啡", 80, 2) == {"item": "咖啡", "price": 80, "quantity": 2, "total": 160}
order = create_order("蛋糕", 120, 3)
assert order["item"] == "蛋糕"
assert order["total"] == 360
# 邊界條件：數量是 0，訂單還是要有完整的四個欄位，總金額是 0
assert create_order("茶", 50, 0) == {"item": "茶", "price": 50, "quantity": 0, "total": 0}
print("✅ 全部通過")
