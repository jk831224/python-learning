Feature: 查訂單

  Scenario: 查得到訂單
    Given 店員已新增訂單：商品 "咖啡"、數量 2、單價 80
    When 店員查訂單 1
    Then 回應代碼是 200
    And 拿回的訂單是 id 1、商品 "咖啡"、數量 2、單價 80、total 160、shipping 60、amount_due 220、status "待付款"

  Scenario: 查不到訂單（邊界條件）
    Given 目前沒有任何訂單
    When 店員查訂單 1
    Then 回應代碼是 404，錯誤訊息是 "查無此訂單"

  # 編號 0 不會是任何訂單的編號（從 1 開始）
  Scenario: 查編號 0（邊界條件）
    Given 店員已新增訂單：商品 "咖啡"、數量 2、單價 80
    When 店員查訂單 0
    Then 回應代碼是 404，錯誤訊息是 "查無此訂單"

  # 有人在網址打了不是數字的編號
  Scenario: 編號不是數字（邊界條件）
    Given 目前沒有任何訂單
    When 店員查訂單 "abc"
    Then 回應代碼是 422
