Feature: 新增訂單

  Scenario: 未滿 500 元，收運費
    Given 目前沒有任何訂單
    When 店員新增訂單：商品 "咖啡"、數量 2、單價 80
    Then 拿回的訂單是 id 1、商品 "咖啡"、數量 2、單價 80、total 160、shipping 60、amount_due 220、status "待付款"

  Scenario: 剛好 500 元，免運（邊界條件）
    Given 目前沒有任何訂單
    When 店員新增訂單：商品 "禮盒"、數量 2、單價 250
    Then 拿回的訂單 total 是 500、shipping 是 0、amount_due 是 500

  Scenario: 已有訂單時，編號接續
    Given 目前已有 2 筆訂單
    When 店員新增訂單：商品 "蛋糕"、數量 1、單價 120
    Then 拿回的訂單 id 是 3
    And 訂單總數變成 3 筆

  Scenario: 單價有小數，四捨五入（邊界條件）
    Given 目前沒有任何訂單
    When 店員新增訂單：商品 "咖啡"、數量 1、單價 80.4
    Then 拿回的訂單 price 是 80

  Scenario: 單價剛好 .5，進位（邊界條件）
    Given 目前沒有任何訂單
    When 店員新增訂單：商品 "咖啡"、數量 2、單價 80.5
    Then 拿回的訂單 price 是 81、total 是 162

  Scenario: 單價是 0（贈品），照規則收運費（邊界條件）
    Given 目前沒有任何訂單
    When 店員新增訂單：商品 "贈品杯墊"、數量 1、單價 0
    Then 拿回的訂單 total 是 0、shipping 是 60、amount_due 是 60

  Scenario: 數量是 0，可以新增（邊界條件）
    Given 目前沒有任何訂單
    When 店員新增訂單：商品 "咖啡"、數量 0、單價 80
    Then 拿回的訂單 total 是 0、shipping 是 60、amount_due 是 60

  Scenario: 數量有小數，新增失敗（邊界條件）
    Given 目前沒有任何訂單
    When 店員新增訂單：商品 "咖啡"、數量 2.4、單價 80
    Then 新增失敗，錯誤訊息是 "數量必須是整數"
    And 訂單總數仍然是 0 筆

  Scenario: 數量是負數，新增失敗（邊界條件）
    Given 目前沒有任何訂單
    When 店員新增訂單：商品 "咖啡"、數量 -1、單價 80
    Then 新增失敗，錯誤訊息是 "數量不能是負數"
    And 訂單總數仍然是 0 筆

  Scenario: 單價是負數，新增失敗（邊界條件）
    Given 目前沒有任何訂單
    When 店員新增訂單：商品 "咖啡"、數量 1、單價 -80
    Then 新增失敗，錯誤訊息是 "單價不能是負數"
    And 訂單總數仍然是 0 筆

  Scenario: 商品名稱是空的，新增失敗（邊界條件）
    Given 目前沒有任何訂單
    When 店員新增訂單：商品 ""、數量 1、單價 80
    Then 新增失敗，錯誤訊息是 "商品名稱不能是空的"
    And 訂單總數仍然是 0 筆

  Scenario: 數量是 2.0，視為整數 2（邊界條件）
    Given 目前沒有任何訂單
    When 店員新增訂單：商品 "咖啡"、數量 2.0、單價 80
    Then 拿回的訂單是 id 1、商品 "咖啡"、數量 2、單價 80、total 160、shipping 60、amount_due 220、status "待付款"

  Scenario: 商品名稱只有空白，新增失敗（邊界條件）
    Given 目前沒有任何訂單
    When 店員新增訂單：商品 "  "、數量 1、單價 80
    Then 新增失敗，錯誤訊息是 "商品名稱不能是空的"
    And 訂單總數仍然是 0 筆

  Scenario: 同時違反兩條規則，回報先檢查到的錯誤（邊界條件）
    Given 目前沒有任何訂單
    When 店員新增訂單：商品 "咖啡"、數量 -2.4、單價 80
    Then 新增失敗，錯誤訊息是 "數量必須是整數"
    And 訂單總數仍然是 0 筆
