"""小店訂單 API（第 1 階段：本機版）。規格見 SPEC.md。"""


def round_half_up(number):
    # 一般的四捨五入（.5 一律進位）；Python 內建 round(80.5) 會得到 80，不符合規格
    # 只用在 0 以上的數：負數在呼叫前就已經被擋掉
    return int(number + 0.5)


def calculate_shipping(total): 
    if total >= 500: #如果總金額大於等於 500 元，則運費為 0
        return 0 #回傳 0    
    return 60 #如果總金額小於 500 元，則運費為 60 元，回傳 60


def add_order(orders, item, quantity, price):
    # 回傳新訂單 dict；輸入不合法時丟出 ValueError，orders 不會被改動
    # 檢查順序照 SPEC「輸入驗證」由上往下，回報第一個遇到的錯誤
    if item.strip() == "": #如果商品名稱是空的，則丟出 ValueError，表示商品名稱不能是空的
        raise ValueError("商品名稱不能是空的")
    if quantity != int(quantity): #如果數量不是整數，則丟出 ValueError，表示數量必須是整數
        raise ValueError("數量必須是整數")
    if quantity < 0: #如果數量是負數，則丟出 ValueError，表示數量不能是負數
        raise ValueError("數量不能是負數")
    if price < 0: #如果單價是負數，則丟出 ValueError，表示單價不能是負數
        raise ValueError("單價不能是負數")
    quantity = int(quantity) #將數量轉換為整數
    price = round_half_up(price) #將單價四捨五入
    total = price * quantity #計算總金額
    shipping = calculate_shipping(total) #計算運費
    new_order = {
        "id": len(orders) + 1, #新訂單的編號是目前的訂單數量 + 1
        "item": item, #商品名稱         
        "quantity": quantity, #數量
        "price": price, #單價
        "total": total, #總金額
        "shipping": shipping, #運費
        "amount_due": total + shipping, #應付金額
        "status": "待付款", #狀態
    }
    orders.append(new_order) #將新訂單加到訂單列表中
    return new_order #回傳新訂單


def find_order(orders, order_id):
    # 回傳符合編號的訂單 dict；找不到時回傳 None
    for order in orders: #逐筆檢查 orders
        if order["id"] == order_id: #如果訂單編號等於 order_id，則回傳那一筆訂單
            return order #回傳那一筆訂單
    return None #如果全部檢查完都沒找到，則回傳 None
