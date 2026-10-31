"""
題目：寫一個計算訂單金額的函式
練習概念：函式（定義函式、參數、回傳值）
為什麼要學：你要做的 API，每一個功能（新增訂單、查訂單）本質上都是一個函式。
           函式的名字和參數，就是「呼叫的人要給什麼、會拿回什麼」的約定。

情境：你在幫一間小店算帳。每筆訂單有「單價」和「數量」，要算出這筆訂單的總金額。
要求：定義一個函式，名字叫 calculate_total，接收兩個參數 price（單價）和 quantity（數量），
      用 return 把總金額交回去。
      注意：是「回傳」，不是 print。
範例：calculate_total(100, 3) → 300
"""

# === 你的答案（從這裡開始寫）===
def calculate_total(price, quantity): # 定義函式，名字叫 calculate_total，接收兩個參數 price（單價）和 quantity（數量）
    return price * quantity # return 回傳值，不是 print 印出來
print(calculate_total(100, 3)) # 呼叫函式，傳入 100 和 3，得到 300
print(calculate_total(25, 4)) # 呼叫函式，傳入 25 和 4，得到 100
print(calculate_total(100, 0)) # 呼叫函式，傳入 100 和 0，得到 0

# === 答案結束 ===

# === 驗收（不用改）===
# 一般情況
assert calculate_total(100, 3) == 300
assert calculate_total(25, 4) == 100
# 邊界條件：數量是 0，總金額應該是 0
assert calculate_total(100, 0) == 0
print("✅ 全部通過")
