"""小店訂單 API（B 階段：網路版）。規格見 SPEC.md。

啟動：uv run python projects/order_api_web/web_api.py，再用瀏覽器打開 http://127.0.0.1:8000
"""

import sqlite3
from pathlib import Path

import uvicorn
from fastapi import FastAPI, HTTPException
from fastapi.responses import HTMLResponse
from pydantic import BaseModel

HERE = Path(__file__).parent

# 狀態機：(現在的狀態, 動作) → 下一個狀態；表上沒有的組合就是「不能走的路」
TRANSITIONS = {
    ("待付款", "付款"): "已付款",
    ("待付款", "取消"): "已取消",
    ("已付款", "取消"): "已退款",
}


class NewOrder(BaseModel):
    # 店員寄來的信；不是數字或缺欄位時，FastAPI 會自動回 422
    # 用 float 而不是 int：數量 2.4 要能收進來，才回得出中文的「數量必須是整數」
    item: str
    quantity: float
    price: float


def round_half_up(number):
    # 一般的四捨五入（.5 一律進位）；Python 內建 round(80.5) 會得到 80，不符合規格
    # 只用在 0 以上的數：負數在呼叫前就已經被擋掉
    return int(number + 0.5)


def calculate_shipping(total):
    if total >= 500:
        return 0
    return 60


def validate(order):
    # 檢查順序照 SPEC「輸入驗證」由上往下，回報第一個遇到的錯誤
    if order.quantity != int(order.quantity):
        return "數量必須是整數"
    if order.quantity < 0:
        return "數量不能是負數"
    if order.price < 0:
        return "單價不能是負數"
    if order.item.strip() == "":
        return "商品名稱不能是空的"
    return None


def create_app(db_path):
    app = FastAPI()

    def connect():
        # 每次都重新連線、重新讀出：拿回去的 dict 被改，不會動到資料庫
        connection = sqlite3.connect(db_path)
        connection.row_factory = sqlite3.Row  # 查出來的每一列可以用欄位名稱取值
        return connection

    def load_order(connection, order_id):
        row = connection.execute("SELECT * FROM orders WHERE id = ?", (order_id,)).fetchone()
        if row is None:
            raise HTTPException(status_code=404, detail="查無此訂單")
        return dict(row)

    def change_status(order_id, action):
        with connect() as connection:
            order = load_order(connection, order_id)
            next_status = TRANSITIONS.get((order["status"], action))
            if next_status is None:
                raise HTTPException(status_code=409, detail=f"{order['status']}的訂單不能{action}")
            connection.execute("UPDATE orders SET status = ? WHERE id = ?", (next_status, order_id))
            return load_order(connection, order_id)

    # 建立 app 時就建好表；表已經存在（程式重新啟動）就保留原本的資料
    # AUTOINCREMENT：編號只往上加，就算以後有刪除，也不會重複發號
    with connect() as connection:
        connection.execute(
            """
            CREATE TABLE IF NOT EXISTS orders (
                id         INTEGER PRIMARY KEY AUTOINCREMENT,
                item       TEXT    NOT NULL,
                quantity   INTEGER NOT NULL,
                price      INTEGER NOT NULL,
                total      INTEGER NOT NULL,
                shipping   INTEGER NOT NULL,
                amount_due INTEGER NOT NULL,
                status     TEXT    NOT NULL
            )
            """
        )

    @app.get("/", response_class=HTMLResponse)
    def clerk_page():
        return (HERE / "clerk_page.html").read_text(encoding="utf-8")

    @app.post("/orders", status_code=201)
    def add_order(order: NewOrder):
        error = validate(order)
        if error is not None:
            raise HTTPException(status_code=400, detail=error)
        quantity = int(order.quantity)
        price = round_half_up(order.price)
        total = price * quantity
        shipping = calculate_shipping(total)
        with connect() as connection:
            cursor = connection.execute(
                "INSERT INTO orders (item, quantity, price, total, shipping, amount_due, status)"
                " VALUES (?, ?, ?, ?, ?, ?, ?)",
                (order.item, quantity, price, total, shipping, total + shipping, "待付款"),
            )
            return load_order(connection, cursor.lastrowid)  # lastrowid：資料庫剛發的編號

    @app.get("/orders/{order_id}")
    def find_order(order_id: int):
        with connect() as connection:
            return load_order(connection, order_id)

    @app.post("/orders/{order_id}/pay")
    def pay_order(order_id: int):
        return change_status(order_id, "付款")

    @app.post("/orders/{order_id}/cancel")
    def cancel_order(order_id: int):
        return change_status(order_id, "取消")

    return app


if __name__ == "__main__":
    uvicorn.run(create_app(HERE / "orders.db"))
