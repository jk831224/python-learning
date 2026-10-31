"""店員程式：在終端機用選單呼叫訂單 API。規格見 SPEC.md「店員程式」。"""

from order_api import add_order, find_order


def to_number(text):
    # 終端機收到的都是文字："2" → 2、"80.5" → 80.5；不是數字就回傳 None
    try:
        return int(text)
    except ValueError:
        pass
    try:
        return float(text)
    except ValueError:
        return None


def handle_add(orders):
    item = input("商品名稱：")
    quantity = to_number(input("數量："))
    price = to_number(input("單價："))
    if quantity is None or price is None:
        print("❌ 請輸入數字")
        return
    try:
        order = add_order(orders, item, quantity, price)
    except ValueError as error:
        # API 拒絕：把 API 給的錯誤訊息原樣顯示
        print(f"❌ {error}")
        return
    print(f"✅ 新增成功：{order}")


def handle_find(orders):
    order_id = to_number(input("訂單編號："))
    if order_id is None:
        print("❌ 請輸入數字")
        return
    order = find_order(orders, order_id)
    if order is None:
        print("❌ 查無此訂單")
        return
    print(f"✅ 查到訂單：{order}")


def main():
    # 第 1 階段的訂單只存在這個 list：程式一關就消失
    orders = []
    while True:
        print()
        print("=== 小店訂單系統 ===")
        print("1. 新增訂單")
        print("2. 查訂單")
        print("3. 離開")
        choice = input("請選擇：")
        if choice == "1":
            handle_add(orders)
        elif choice == "2":
            handle_find(orders)
        elif choice == "3":
            print("再見！")
            return
        else:
            print("❌ 請輸入 1、2 或 3")


main()
