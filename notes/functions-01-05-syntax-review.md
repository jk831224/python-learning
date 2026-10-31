# 複習：函式練習 01–05 用到的 Python 語法

這份不用背。目標是**看到程式碼能翻成一句中文**。你用 AI Tab 補完程式碼時，也可以照這份把補出來的每一行翻成白話；翻得出來，代表你看懂了，翻不出來，就回來查這份。

---

## 速查表

| # | 語法 | 長相 | 白話翻譯 | 第一次出現 |
|---|---|---|---|---|
| 1 | 定義函式 | `def 名字(參數):` | 「我要定義一個叫『名字』的功能，它收這些東西」 | 01 |
| 2 | 縮排 | 行首空 4 格 | 「這行屬於上面那一層」 | 01 |
| 3 | 回傳 | `return 值` | 「把這個值交回給呼叫的人，然後結束」 | 01 |
| 4 | 呼叫函式 | `名字(值, 值)` | 「叫『名字』這個功能做事，把這些值交給它」 | 01 |
| 5 | 變數 | `名字 = 值` | 「把右邊的值存進叫『名字』的盒子」 | 03 |
| 6 | dict | `{"key": 值}` | 「一張有欄位名稱的表單」 | 02 |
| 7 | 從 dict 取值 | `order["item"]` | 「拿 order 這張表單的 item 欄」 | 02（驗收區） |
| 8 | if 判斷 | `if 條件:` | 「如果條件成立，就做下面縮排的事」 | 03（已提供區） |
| 9 | 比較 | `==`、`>=` | 「等不等於」「大於等於」 | 03、04 |
| 10 | list | `[a, b, c]` | 「一排按順序放的東西」 | 04 |
| 11 | for 迴圈 | `for x in 清單:` | 「從清單裡一個一個拿出來，每次叫它 x」 | 04 |
| 12 | None | `None` | 「什麼都沒有」 | 04 |
| 13 | 長度 | `len(清單)` | 「清單裡有幾個」 | 05 |
| 14 | 加到最後面 | `清單.append(值)` | 「把值加到清單最後面」 | 05 |
| 15 | 取最後一個 | `清單[-1]` | 「清單的最後一個」 | 05（驗收區） |
| 16 | 驗收 | `assert 條件` | 「條件必須成立，不成立就報錯停下來」 | 每題驗收區 |

下面依題目順序，一個一個說明。

---

## 01：函式的骨架

```python
def calculate_total(price, quantity):
    return price * quantity
```

逐行翻譯：

| 程式碼 | 白話 |
|---|---|
| `def` | 「我要定義一個函式」 |
| `calculate_total` | 函式的名字，之後用這個名字叫它 |
| `(price, quantity)` | 它收兩樣東西，進來後分別叫 price、quantity（叫做**參數**） |
| `:` | 「函式的內容從下一行開始」 |
| 行首 4 格空白 | 「這行屬於上面的函式」 |
| `return price * quantity` | 「把 price 乘 quantity 的結果交回去」 |

**參數**：函式的「收件欄位」。就像點餐單上的「品項」「數量」兩格，客人每次填不同的值，但格子名稱固定。

### 縮排決定「屬於誰」

Python 不用大括號，靠**行首空幾格**決定哪幾行屬於同一塊。往右縮一層 = 「我屬於上面那行」；縮回來 = 「那一塊結束了」。

```python
def calculate_total(price, quantity):
    return price * quantity      ← 縮 4 格：屬於函式


print(calculate_total(100, 3))   ← 沒縮：不屬於函式，是函式外面的程式
```

### `return` 和 `print` 的差別

- `print(x)`：把 x **印在畫面上給人看**。程式拿不到這個值。
- `return x`：把 x **交回給呼叫的人**。呼叫的人可以拿去存、拿去比對。

驗收區的 `assert calculate_total(100, 3) == 300` 能運作，是因為 `return` 把 300 交回來了。

---

## 02：dict，一張有欄位名的表單

```python
def create_order(item, price, quantity):
    return {
        "item": item,
        "price": price,
        "quantity": quantity,
        "total": price * quantity,
    }
```

**dict**：用「欄位名 → 值」存資料的容器。像一張填好的表單：左邊是印好的欄位名稱，右邊是填進去的內容。

拆開看其中一行：

```python
"item": item,
```

| 部分 | 意思 |
|---|---|
| `"item"`（有引號） | **欄位名稱**（key），是固定的文字 |
| `:` | 「對應到」 |
| `item`（沒引號） | **參數**，是呼叫時傳進來的值，例如 `"咖啡"` |
| `,` | 「下一個欄位」 |

**有引號 vs 沒引號**是讀 dict 最重要的分辨：有引號是寫死的文字，沒引號是變數（會換成裡面裝的值）。

### 從 dict 取值

```python
order = create_order("蛋糕", 120, 3)
order["item"]    # → "蛋糕"
order["total"]   # → 360
```

翻譯：「拿 order 這張表單的 item 欄」。中括號裡放欄位名稱，要和建立時寫的一字不差。

---

## 03：變數，以及函式呼叫函式

```python
def create_order(item, price, quantity):
    total = calculate_total(price, quantity)
    shipping = calculate_shipping(total)
    return {
        "item": item,
        "quantity": quantity,
        "total": total,
        "shipping": shipping,
        "amount_due": total + shipping,
    }
```

### 變數：`=` 是「存進去」，不是「等於」

```python
total = calculate_total(price, quantity)
```

**從右邊讀到左邊**：「先呼叫 calculate_total 算出結果，再把結果存進叫 total 的盒子」。之後寫 `total`，就是拿出盒子裡的值。

**變數**：貼了標籤的盒子。值放進去後，用標籤名就能拿出來，不用每次重算。

### 函式呼叫函式

`create_order` 自己不算金額，它請 `calculate_total` 算，拿回結果後再交給 `calculate_shipping`。讀的時候照**由上往下**的順序，把每一行當成一站：

1. 第 1 站：算總金額 → 存進 `total`
2. 第 2 站：拿 `total` 去算運費 → 存進 `shipping`
3. 第 3 站：把結果組成 dict 交回去

### if：已提供區的 `calculate_shipping`

```python
def calculate_shipping(total):
    if total >= 500:
        return 0
    return 60
```

翻譯：「如果 total 大於等於 500，就交回 0（結束）。沒進到 if 的話，交回 60。」

這裡沒寫 `else`，卻能正確運作，原因是 `return` 一執行函式就結束。進到 if 的人已經在 `return 0` 離開了，能走到 `return 60` 的，一定是沒進 if 的。

---

## 04：list、for 迴圈、None

```python
orders = [
    {"id": 1, "item": "咖啡", "status": "待付款"},
    {"id": 2, "item": "蛋糕", "status": "已付款"},
    {"id": 3, "item": "禮盒", "status": "已出貨"},
]
```

**list**：按順序排好的一排東西，用 `[ ]` 包起來、逗號隔開。這裡每個東西都是一個 dict，所以 `orders` 是「一疊表單」。

```python
def find_order(orders, order_id):
    for order in orders:
        if order["id"] == order_id:
            return order
    return None
```

逐行翻譯：

| 程式碼 | 白話 |
|---|---|
| `for order in orders:` | 「從 orders 這疊表單裡，一張一張拿出來，每次拿到的那張叫 order」 |
| `if order["id"] == order_id:` | 「如果這張的 id 欄等於要找的編號」 |
| `return order` | 「交回這張，函式結束（剩下的不看了）」 |
| `return None` | 「（全部看完都沒找到）交回『什麼都沒有』」 |

### 從縮排看出結構

```python
def find_order(orders, order_id):       ← 第 0 層：函式
    for order in orders:                ← 第 1 層：屬於函式
        if order["id"] == order_id:     ← 第 2 層：屬於迴圈，每一圈都會做
            return order                ← 第 3 層：屬於 if，條件成立才做
    return None                         ← 第 1 層：迴圈結束後才做
```

`return None` 和 `for` 對齊，所以它在迴圈**外面**，迴圈全部跑完才會輪到它。

### `=` 和 `==`

- `=`：存進去（`total = 160`）
- `==`：問「相不相等？」，答案是 True 或 False（`order["id"] == 2`）

### None 與 `is None`

**None**：Python 的「空」。像查詢結果上蓋的「查無此筆」章。

驗收區寫 `find_order(orders, 99) is None`，翻譯是「拿回來的是不是『什麼都沒有』」。檢查 None 時習慣用 `is`，不用 `==`。

---

## 05：len、append，以及「函式改到外面的東西」

你提到 05 開始讀起來吃力。這題確實一次疊了好幾層：dict 放在變數裡、方法呼叫（`.append`）、而且函式會改到外面的 list。下面一層一層拆。

```python
def add_order(orders, item):
    new_order = {
        "id": len(orders) + 1,
        "item": item,
        "status": "待付款",
    }
    orders.append(new_order)
    return new_order
```

### 第 1 塊：組一張新表單，存進 `new_order`

```python
new_order = {
    "id": len(orders) + 1,
    "item": item,
    "status": "待付款",
}
```

雖然有 5 行，但它**只是一句話**：「組一個 dict，存進 new_order」。`{` 開頭到 `}` 結尾都是同一個 dict，換行只是為了好讀。

裡面三個欄位：

| 欄位 | 值 | 白話 |
|---|---|---|
| `"id"` | `len(orders) + 1` | 「現在有幾筆，再加 1」 |
| `"item"` | `item` | 「呼叫時傳進來的商品名」（沒引號 → 是參數） |
| `"status"` | `"待付款"` | 「固定寫死『待付款』」（有引號 → 是文字） |

`len(orders)`：**len** 是 length（長度）的縮寫，交回「清單裡有幾個」。orders 有 3 筆時，`len(orders)` 是 3，加 1 就是 4。

### 第 2 塊：`.append`，把表單放進那一疊

```python
orders.append(new_order)
```

翻譯：「對 orders 這疊表單做 append（加到最後面），加的是 new_order」。

這裡第一次出現 `東西.動作(值)` 這種寫法，叫做**方法**。

**方法**：某種東西「自己會做的事」。像「遙控器.開機()」：開機是遙控器的功能，寫法是先講主角、加一個點、再講動作。list 自己會做的事包括 `append`（加到最後）等等。

和前面的函式對照：

| 寫法 | 例子 | 讀法 |
|---|---|---|
| 函式 | `len(orders)` | 「叫 len 來量 orders」 |
| 方法 | `orders.append(x)` | 「叫 orders 自己把 x 加進去」 |

### 第 3 塊：交回新表單

```python
return new_order
```

交回剛組好的那張。呼叫的人就能知道新訂單拿到幾號。

### 05 最容易卡住的地方：函式改到了外面的 list

前四題的函式都是「收東西 → 算 → 交回去」，外面的東西不會變。05 不一樣：

```python
orders = [ ...3 筆... ]          # 函式外面的 list
add_order(orders, "馬卡龍")       # 把 orders 交給函式
len(orders)                       # → 4，外面的 list 變了！
```

原因是：把 list 傳進函式時，**交出去的是同一疊表單本身，不是影印本**。函式裡的 `orders.append(...)`，就是直接在那一疊上加一張。所以函式結束後，外面的 `orders` 也多了一筆。

這正是 05 想要的效果：新訂單要真的「存起來」，之後用 `find_order` 才查得到。

### 驗收區的 `orders[-1]`

```python
assert orders[-1] == {"id": 4, "item": "馬卡龍", "status": "待付款"}
```

`清單[數字]` 是「拿第幾個」。正數從頭數（`[0]` 是第一個），負數從尾巴數（`[-1]` 是最後一個）。所以這行是：「orders 的最後一筆，必須是剛新增的馬卡龍」。

---

## 每題都有的：`assert`

```python
assert calculate_total(100, 3) == 300
```

翻譯：「我斷定 calculate_total(100, 3) 會等於 300；不是的話就報錯停下來」。

**assert**：自動驗收員。條件成立就安靜放行；不成立就喊停，並指出是哪一行。驗收區全部安靜跑完，才會印出 `✅ 全部通過`。

---

## 讀不懂一行程式時，照這個順序拆

1. **看縮排**：這行屬於哪一層（函式裡？迴圈裡？if 裡？）
2. **找** `=`：有 `=` 的話，先讀右邊（算出什麼），再讀左邊（存進哪裡）
3. **分辨有沒有引號**：有引號是寫死的文字，沒引號是變數或參數
4. **看括號前面是什麼**：
   - `名字(...)` → 呼叫函式
   - `東西.名字(...)` → 叫「東西」做某個動作（方法）
   - `東西[...]` → 從「東西」裡拿一格（dict 拿欄位、list 拿第幾個）
5. **翻成一句中文**：翻得通，就是看懂了
