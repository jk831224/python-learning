"""六個 .feature 共用的 step definitions：把 Gherkin 的每一句對應到 Python。

測試對實作的要求（實作要照這份做，測試才接得上）：

- web_api.py 提供 create_app(db_path)：回傳 FastAPI app，訂單存在 db_path 這個 SQLite 檔。
  建立 app 時就要建好 orders 表，欄位照 schema.dbml。
- 店員網頁（GET /）：
  - 兩個區塊，名稱是「新增訂單」「查詢訂單」
  - 新增區有「商品」「數量」「單價」三個欄位和「新增」按鈕；查詢區有「訂單編號」欄位和「查詢」按鈕
  - 訂單用表格顯示，每一列左邊是欄位中文名（th），右邊是值（td）
  - 「付款」「取消」按鈕
  - 錯誤訊息放在 role="alert" 的元素裡，紅字
"""

import re
import socket
import sqlite3
import threading
import time

import pytest
import uvicorn
from fastapi.testclient import TestClient
from playwright.sync_api import expect
from pytest_bdd import given, parsers, then, when

ORDER_ARGS = r'商品 "(?P<item>[^"]*)"、數量 (?P<quantity>"[^"]*"|-?[\d.]+)、單價 (?P<price>"[^"]*"|-?[\d.]+)'


def to_value(text):
    # "2" → 2、"2.4" → 2.4；有引號的 "\"abc\"" → "abc"，照原樣寄給 API
    if text.startswith('"'):
        return text.strip('"')
    if "." in text:
        return float(text)
    return int(text)


def make_client(db_path):
    # 在這裡才 import：web_api.py 還沒寫的時候，每個 Scenario 各自失敗（red），而不是整批無法收集
    from web_api import create_app

    return TestClient(create_app(db_path))


def insert_order(db_path, id, status):
    # 直接寫進資料庫，不經過 API，讓 Given 不依賴待測的實作
    with sqlite3.connect(db_path) as connection:
        connection.execute(
            "INSERT INTO orders (id, item, quantity, price, total, shipping, amount_due, status)"
            " VALUES (?, ?, 2, 80, 160, 60, 220, ?)",
            (id, f"商品{id}", status),
        )


@pytest.fixture
def order_context(tmp_path):
    # 每個 Scenario 一個全新的暫存資料庫，Scenario 之間互不影響，也不碰 orders.db
    db_path = tmp_path / "test.db"
    return {"db_path": db_path, "client": make_client(db_path), "response": None, "dialogs": []}


@pytest.fixture
def live_server(order_context):
    # 網頁測試要真的開門營業：瀏覽器只能透過網址連進來，不能用 TestClient
    from web_api import create_app

    with socket.socket() as sock:
        sock.bind(("127.0.0.1", 0))
        port = sock.getsockname()[1]
    server = uvicorn.Server(uvicorn.Config(create_app(order_context["db_path"]), port=port, log_level="warning"))
    thread = threading.Thread(target=server.run, daemon=True)
    thread.start()
    deadline = time.time() + 10
    while not server.started:
        assert time.time() < deadline, "伺服器 10 秒內沒有啟動"
        time.sleep(0.05)
    yield f"http://127.0.0.1:{port}"
    server.should_exit = True
    thread.join()


# === Given：準備資料 ===


@given("目前沒有任何訂單")
def no_orders(order_context):
    # order_context 本來就是空的暫存資料庫，什麼都不用做
    pass


@given(parsers.re(r"目前已有 (?P<count>\d+) 筆訂單"))
def existing_orders(order_context, count):
    for id in range(1, int(count) + 1):
        insert_order(order_context["db_path"], id, "待付款")


@given(parsers.re(r'訂單 (?P<order_id>\d+) 的狀態是 "(?P<status>[^"]*)"'))
def order_with_status(order_context, order_id, status):
    insert_order(order_context["db_path"], int(order_id), status)


@given(parsers.re(r"店員已新增訂單：" + ORDER_ARGS))
def order_added(order_context, item, quantity, price):
    response = order_context["client"].post(
        "/orders", json={"item": item, "quantity": to_value(quantity), "price": to_value(price)}
    )
    assert response.status_code == 201, f"準備資料時新增失敗：{response.text}"


# === When：店員寄信給 API ===


@when(parsers.re(r"店員送出新增訂單：" + ORDER_ARGS))
def clerk_adds_order(order_context, item, quantity, price):
    order_context["response"] = order_context["client"].post(
        "/orders", json={"item": item, "quantity": to_value(quantity), "price": to_value(price)}
    )


@when(parsers.re(r'店員送出新增訂單：只有商品 "(?P<item>[^"]*)"、數量 (?P<quantity>-?[\d.]+)，沒有單價'))
def clerk_adds_order_without_price(order_context, item, quantity):
    order_context["response"] = order_context["client"].post("/orders", json={"item": item, "quantity": to_value(quantity)})


@when(parsers.re(r'店員查訂單 (?P<order_id>\d+|"[^"]*")'))
def clerk_finds_order(order_context, order_id):
    # 編號寫在網址上；"abc" 也照樣放進網址，看 API 怎麼回
    order_context["response"] = order_context["client"].get(f"/orders/{order_id.strip('"')}")


@given(parsers.re(r"店員對訂單 (?P<order_id>\d+) 付款"))
@when(parsers.re(r"店員對訂單 (?P<order_id>\d+) 付款"))
def clerk_pays(order_context, order_id):
    order_context["response"] = order_context["client"].post(f"/orders/{order_id}/pay")


@when(parsers.re(r"店員取消訂單 (?P<order_id>\d+)"))
def clerk_cancels(order_context, order_id):
    order_context["response"] = order_context["client"].post(f"/orders/{order_id}/cancel")


@when("API 程式重新啟動")
def restart(order_context):
    # 用同一個資料庫檔重新建一個 app，等於把程式關掉再打開
    order_context["client"] = make_client(order_context["db_path"])


# === Then：檢查 API 的回信 ===


@then(parsers.re(r"回應代碼是 (?P<code>\d+)"))
def status_code_is(order_context, code):
    assert order_context["response"].status_code == int(code), order_context["response"].text


@then(parsers.re(r'回應代碼是 (?P<code>\d+)，錯誤訊息是 "(?P<message>[^"]*)"'))
def failed_with(order_context, code, message):
    assert order_context["response"].status_code == int(code), order_context["response"].text
    assert order_context["response"].json() == {"detail": message}


@then(
    parsers.re(
        r'拿回的訂單是 id (?P<id>\d+)、商品 "(?P<item>[^"]*)"、數量 (?P<quantity>\d+)、單價 (?P<price>\d+)、'
        r'total (?P<total>\d+)、shipping (?P<shipping>\d+)、amount_due (?P<amount_due>\d+)、status "(?P<status>[^"]*)"'
    )
)
def order_is(order_context, id, item, quantity, price, total, shipping, amount_due, status):
    assert order_context["response"].json() == {
        "id": int(id),
        "item": item,
        "quantity": int(quantity),
        "price": int(price),
        "total": int(total),
        "shipping": int(shipping),
        "amount_due": int(amount_due),
        "status": status,
    }


@then(parsers.re(r"拿回的訂單 total 是 (?P<total>\d+)、shipping 是 (?P<shipping>\d+)、amount_due 是 (?P<amount_due>\d+)"))
def order_amounts_are(order_context, total, shipping, amount_due):
    order = order_context["response"].json()
    assert order["total"] == int(total)
    assert order["shipping"] == int(shipping)
    assert order["amount_due"] == int(amount_due)


@then(parsers.re(r"拿回的訂單 id 是 (?P<id>\d+)"))
def order_id_is(order_context, id):
    assert order_context["response"].json()["id"] == int(id)


@then(parsers.re(r"拿回的訂單 price 是 (?P<price>\d+)"))
def order_price_is(order_context, price):
    # 用 type 確認是整數：80.0 雖然 == 80，但不符合「金額都是整數」
    order = order_context["response"].json()
    assert order["price"] == int(price)
    assert type(order["price"]) is int


@then(parsers.re(r"拿回的訂單 price 是 (?P<price>\d+)、total 是 (?P<total>\d+)"))
def order_price_and_total_are(order_context, price, total):
    order = order_context["response"].json()
    assert order["price"] == int(price)
    assert type(order["price"]) is int
    assert order["total"] == int(total)


@then(parsers.re(r'拿回的訂單 status 是 "(?P<status>[^"]*)"'))
def order_status_is(order_context, status):
    assert order_context["response"].json()["status"] == status


@then(parsers.re(r'再查訂單 (?P<order_id>\d+)，status 是 "(?P<status>[^"]*)"'))
def status_after_find_is(order_context, order_id, status):
    # 不看剛才的回信，重新查一次，確認資料庫裡真的是這個狀態
    response = order_context["client"].get(f"/orders/{order_id}")
    assert response.json()["status"] == status


@then(parsers.re(r"資料庫裡的訂單總數是 (?P<count>\d+) 筆"))
def order_count_is(order_context, count):
    with sqlite3.connect(order_context["db_path"]) as connection:
        assert connection.execute("SELECT COUNT(*) FROM orders").fetchone()[0] == int(count)


# === 店員網頁：用瀏覽器操作 ===


def shown_value(page, label):
    # 訂單表格裡，左邊寫著 label 的那一列，右邊的值
    return page.locator(f'tr:has(th:text-is("{label}")) td')


def open_page(order_context, page, live_server):
    # 記下所有彈出視窗；有人監聽時 Playwright 不會自動關掉，所以要自己關
    page.on("dialog", lambda dialog: (order_context["dialogs"].append(dialog.type), dialog.dismiss()))
    page.goto(live_server)


def find_on_page(page, order_id):
    area = page.get_by_role("region", name="查詢訂單")
    area.get_by_label("訂單編號").fill(order_id)
    area.get_by_role("button", name="查詢").click()


@given("店員打開網頁")
def clerk_opens_page(order_context, page, live_server):
    open_page(order_context, page, live_server)


@given(parsers.re(r"店員打開網頁，查到訂單 (?P<order_id>\d+)"))
def clerk_opens_page_and_finds(order_context, page, live_server, order_id):
    open_page(order_context, page, live_server)
    find_on_page(page, order_id)
    expect(shown_value(page, "訂單編號")).to_have_text(order_id)


@when(parsers.re(r'店員在新增區填入商品 "(?P<item>[^"]*)"、數量 "(?P<quantity>[^"]*)"、單價 "(?P<price>[^"]*)"，按下「新增」'))
def clerk_fills_add_form(page, item, quantity, price):
    area = page.get_by_role("region", name="新增訂單")
    area.get_by_label("商品").fill(item)
    area.get_by_label("數量").fill(quantity)
    area.get_by_label("單價").fill(price)
    area.get_by_role("button", name="新增").click()


@when(parsers.re(r'店員在新增區填入商品 "(?P<item>[^"]*)"、數量 "(?P<quantity>[^"]*)"，單價留空，按下「新增」'))
def clerk_fills_add_form_without_price(page, item, quantity):
    area = page.get_by_role("region", name="新增訂單")
    area.get_by_label("商品").fill(item)
    area.get_by_label("數量").fill(quantity)
    area.get_by_role("button", name="新增").click()


@when(parsers.re(r'店員在查詢區填入訂單編號 "(?P<order_id>[^"]*)"，按下「查詢」'))
def clerk_fills_find_form(page, order_id):
    find_on_page(page, order_id)


@when(parsers.re(r"店員按下「(?P<button>付款|取消)」"))
def clerk_clicks(page, button):
    page.get_by_role("button", name=button).click()


@then(parsers.re(r"畫面顯示訂單編號 (?P<order_id>\d+)"))
def page_shows_order_id(page, order_id):
    expect(shown_value(page, "訂單編號")).to_have_text(order_id)


@then(parsers.re(r'畫面顯示小計 (?P<total>\d+)、運費 (?P<shipping>\d+)、應付金額 (?P<amount_due>\d+)、狀態 "(?P<status>[^"]*)"'))
def page_shows_amounts(page, total, shipping, amount_due, status):
    expect(shown_value(page, "小計")).to_have_text(total)
    expect(shown_value(page, "運費")).to_have_text(shipping)
    expect(shown_value(page, "應付金額")).to_have_text(amount_due)
    expect(shown_value(page, "狀態")).to_have_text(status)


@then(parsers.re(r'畫面顯示訂單編號 (?P<order_id>\d+)、商品 "(?P<item>[^"]*)"、應付金額 (?P<amount_due>\d+)、狀態 "(?P<status>[^"]*)"'))
def page_shows_order(page, order_id, item, amount_due, status):
    expect(shown_value(page, "訂單編號")).to_have_text(order_id)
    expect(shown_value(page, "商品")).to_have_text(item)
    expect(shown_value(page, "應付金額")).to_have_text(amount_due)
    expect(shown_value(page, "狀態")).to_have_text(status)


@then(parsers.re(r'畫面顯示狀態 "(?P<status>[^"]*)"'))
def page_shows_status(page, status):
    expect(shown_value(page, "狀態")).to_have_text(status)


@then(parsers.re(r'畫面用紅字顯示 "(?P<message>[^"]*)"'))
def page_shows_red_error(page, message):
    error = page.get_by_role("alert").filter(has_text=message)
    expect(error).to_be_visible()
    # 紅字：瀏覽器算出來的文字顏色，紅色成分高、綠和藍成分低
    color = error.evaluate("element => getComputedStyle(element).color")
    red, green, blue = (int(n) for n in re.findall(r"\d+", color)[:3])
    assert red >= 150 and green <= 80 and blue <= 80, f"文字顏色是 {color}，不是紅色"


@then(parsers.re(r'畫面上有 "(?P<text>[^"]*)"'))
def page_has_text(page, text):
    expect(page.locator("body")).to_contain_text(text)


@then(parsers.re(r'畫面上沒有 "(?P<text>[^"]*)"'))
def page_has_no_text(page, text):
    expect(page.locator("body")).not_to_contain_text(text)


@then("沒有跳出任何彈出視窗")
def no_dialogs(order_context):
    assert order_context["dialogs"] == []
