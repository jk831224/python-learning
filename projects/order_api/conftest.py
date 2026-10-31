"""兩個 .feature 共用的 step definitions：把 Gherkin 的每一句對應到 Python。"""

import pytest
from pytest_bdd import given, parsers, then, when

from order_api import add_order, find_order


def to_number(text):
    # "2" → 2、"2.4" → 2.4、"-1" → -1：照店員輸入的樣子交給 API
    if "." in text:
        return float(text)
    return int(text)


@pytest.fixture
def context():
    # 每個 Scenario 一份全新的資料，Scenario 之間互不影響
    return {"orders": [], "result": None, "error": None, "added": None}


# === Given ===


@given("目前沒有任何訂單")
def no_orders(context):
    context["orders"] = []


@given(parsers.re(r"目前已有 (?P<count>\d+) 筆訂單"))
def existing_orders(context, count):
    # 直接放入現成的訂單，不經過 add_order，讓 Given 不依賴待測的實作
    context["orders"] = [
        {
            "id": i,
            "item": f"商品{i}",
            "quantity": 1,
            "price": 100,
            "total": 100,
            "shipping": 60,
            "amount_due": 160,
            "status": "待付款",
        }
        for i in range(1, int(count) + 1)
    ]


@given(parsers.re(r'已新增一筆訂單：商品 "(?P<item>[^"]*)"、數量 (?P<quantity>-?[\d.]+)、單價 (?P<price>-?[\d.]+)'))
def order_added(context, item, quantity, price):
    context["added"] = add_order(context["orders"], item, to_number(quantity), to_number(price))


# === When ===


@when(parsers.re(r'店員新增訂單：商品 "(?P<item>[^"]*)"、數量 (?P<quantity>-?[\d.]+)、單價 (?P<price>-?[\d.]+)'))
def clerk_adds_order(context, item, quantity, price):
    try:
        context["result"] = add_order(context["orders"], item, to_number(quantity), to_number(price))
    except ValueError as error:
        context["error"] = error


@when(parsers.re(r"店員查編號 (?P<order_id>\d+)"))
def clerk_finds_order(context, order_id):
    context["result"] = find_order(context["orders"], int(order_id))


# === Then ===


@then(
    parsers.re(
        r'拿回的訂單是 id (?P<id>\d+)、商品 "(?P<item>[^"]*)"、數量 (?P<quantity>\d+)、單價 (?P<price>\d+)、'
        r'total (?P<total>\d+)、shipping (?P<shipping>\d+)、amount_due (?P<amount_due>\d+)、status "(?P<status>[^"]*)"'
    )
)
def order_is(context, id, item, quantity, price, total, shipping, amount_due, status):
    assert context["result"] == {
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
def order_amounts_are(context, total, shipping, amount_due):
    assert context["result"]["total"] == int(total)
    assert context["result"]["shipping"] == int(shipping)
    assert context["result"]["amount_due"] == int(amount_due)


@then(parsers.re(r"拿回的訂單 id 是 (?P<id>\d+)"))
def order_id_is(context, id):
    assert context["result"]["id"] == int(id)


@then(parsers.re(r"拿回的訂單 price 是 (?P<price>\d+)"))
def order_price_is(context, price):
    # 用 type 確認是整數：80.0 雖然 == 80，但不符合「金額都是整數」
    assert context["result"]["price"] == int(price)
    assert type(context["result"]["price"]) is int


@then(parsers.re(r"拿回的訂單 price 是 (?P<price>\d+)、total 是 (?P<total>\d+)"))
def order_price_and_total_are(context, price, total):
    assert context["result"]["price"] == int(price)
    assert type(context["result"]["price"]) is int
    assert context["result"]["total"] == int(total)


@then(parsers.re(r"訂單總數(?:變成|仍然是) (?P<count>\d+) 筆"))
def order_count_is(context, count):
    assert len(context["orders"]) == int(count)


@then(parsers.re(r'新增失敗，錯誤訊息是 "(?P<message>[^"]*)"'))
def add_failed_with(context, message):
    assert context["error"] is not None, "預期新增失敗（ValueError），但沒有失敗"
    assert str(context["error"]) == message


@then("拿回的訂單和新增時拿回的完全相同")
def same_as_added(context):
    assert context["result"] == context["added"]


@then("拿回 None")
def got_none(context):
    assert context["result"] is None
