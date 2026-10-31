"""小店訂單 API（第 1 階段：本機版）。規格見 SPEC.md。"""


def round_half_up(number):
    # 一般的四捨五入（.5 一律進位）；Python 內建 round(80.5) 會得到 80，不符合規格
    # 只用在 0 以上的數：負數在呼叫前就已經被擋掉
    return int(number + 0.5)


def calculate_shipping(total):
    if total >= 500:
        return 0
    return 60


def add_order(orders, item, quantity, price):
    # 回傳新訂單 dict；輸入不合法時丟出 ValueError，orders 不會被改動
    # 檢查順序照 SPEC「輸入驗證」由上往下，回報第一個遇到的錯誤
    if item == "":
        raise ValueError("商品名稱不能是空的")
    if quantity != int(quantity):
        raise ValueError("數量必須是整數")
    if quantity < 0:
        raise ValueError("數量不能是負數")
    if price < 0:
        raise ValueError("單價不能是負數")

    quantity = int(quantity)
    price = round_half_up(price)
    total = price * quantity
    shipping = calculate_shipping(total)
    new_order = {
        "id": len(orders) + 1,
        "item": item,
        "quantity": quantity,
        "price": price,
        "total": total,
        "shipping": shipping,
        "amount_due": total + shipping,
        "status": "待付款",
    }
    orders.append(new_order)
    return new_order


def find_order(orders, order_id):
    # 回傳符合編號的訂單 dict；找不到時回傳 None
    for order in orders:
        if order["id"] == order_id:
            return order
    return None
