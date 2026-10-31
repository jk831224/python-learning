"""
題目：在函式裡呼叫其他函式，算出含運費的訂單
練習概念：函式呼叫函式（把小功能組合成大功能）
為什麼要學：你的 API「新增訂單」不會把所有計算塞在同一個函式裡，
           而是交給好幾個小函式各算一部分，再組合成一筆訂單。

情境：小店開始收運費。商品總金額滿 500 元免運，未滿 500 元收 60 元運費。
      「算總金額」和「算運費」這兩個小函式已經寫好了（在下方「已提供」區），你不用重寫。
要求：定義一個函式 create_order(item, price, quantity)，在裡面「呼叫」已提供的兩個函式，
      回傳一個 dict，裡面要有五個欄位：
        "item"       → 商品名稱
        "quantity"   → 數量
        "total"      → 商品總金額（呼叫 calculate_total 算）
        "shipping"   → 運費（把 total 交給 calculate_shipping 算）
        "amount_due" → 應付金額（total + shipping）
輔助材料：同資料夾的 03_order_with_shipping.md，畫出資料在三個函式之間怎麼傳。

Feature: 建立含運費的訂單

  Scenario: 未滿 500 元，要收運費
    Given 單價 80 元的咖啡
    When 買 2 杯
    Then total 是 160，shipping 是 60，amount_due 是 220

  Scenario: 滿 500 元以上，免運
    Given 單價 300 元的蛋糕
    When 買 2 個
    Then total 是 600，shipping 是 0，amount_due 是 600

  Scenario: 剛好 500 元（邊界條件），算「滿」，免運
    Given 單價 250 元的禮盒
    When 買 2 盒
    Then total 是 500，shipping 是 0，amount_due 是 500
"""

# === 已提供（不用改）===
def calculate_total(price, quantity): #定義一個函式，名字叫 calculate_total，接收兩個參數 price（單價）、quantity（數量），回傳一個數字，表示商品總金額（單價 × 數量）
    return price * quantity #商品總金額（單價 × 數量）


def calculate_shipping(total): #定義一個函式，名字叫 calculate_shipping，接收一個參數 total（商品總金額），回傳一個數字，表示運費
    if total >= 500: #如果商品總金額大於等於 500 元，則運費為 0
        return 0
    return 60 #如果商品總金額小於 500 元，則運費為 60 元


# === 你的答案（從這裡開始寫）===
def create_order(item, price, quantity):
    # 先算一次、存進變數，後面直接用變數，不重複呼叫同一個函式
    total = calculate_total(price, quantity)  # 第 1 站：算商品總金額
    shipping = calculate_shipping(total)  # 第 2 站：上一站的 total 變成這裡的輸入
    return {  # 第 3 站：把結果組成一筆訂單（key 照題目約定）
        "item": item,
        "quantity": quantity,
        "total": total,
        "shipping": shipping,
        "amount_due": total + shipping,
    }


print(create_order("咖啡", 80, 2))
print(create_order("蛋糕", 300, 2))
print(create_order("禮盒", 250, 2))
print(create_order("PS5", 36000, 1))

# === 答案結束 ===

# === 驗收（不用改）===
# Scenario: 未滿 500 元，要收運費
assert create_order("咖啡", 80, 2) == {
    "item": "咖啡", "quantity": 2, "total": 160, "shipping": 60, "amount_due": 220
}
# Scenario: 滿 500 元以上，免運
assert create_order("蛋糕", 300, 2) == {
    "item": "蛋糕", "quantity": 2, "total": 600, "shipping": 0, "amount_due": 600
}
# Scenario: 剛好 500 元（邊界條件），算「滿」，免運
assert create_order("禮盒", 250, 2) == {
    "item": "禮盒", "quantity": 2, "total": 500, "shipping": 0, "amount_due": 500
}
print("✅ 全部通過")
