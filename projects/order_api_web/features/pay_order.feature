Feature: 付款

  Scenario: 待付款的訂單付款
    Given 訂單 1 的狀態是 "待付款"
    When 店員對訂單 1 付款
    Then 回應代碼是 200
    And 拿回的訂單 status 是 "已付款"
    And 再查訂單 1，status 是 "已付款"

  # 狀態變了，金額不能跟著亂掉
  Scenario: 付款後，其他欄位不變（邊界條件）
    Given 店員已新增訂單：商品 "咖啡"、數量 2、單價 80
    When 店員對訂單 1 付款
    Then 拿回的訂單是 id 1、商品 "咖啡"、數量 2、單價 80、total 160、shipping 60、amount_due 220、status "已付款"

  Scenario: 已付款的訂單不能再付款（邊界條件）
    Given 訂單 1 的狀態是 "已付款"
    When 店員對訂單 1 付款
    Then 回應代碼是 409，錯誤訊息是 "已付款的訂單不能付款"
    And 再查訂單 1，status 是 "已付款"

  Scenario: 已取消的訂單不能付款（邊界條件）
    Given 訂單 1 的狀態是 "已取消"
    When 店員對訂單 1 付款
    Then 回應代碼是 409，錯誤訊息是 "已取消的訂單不能付款"
    And 再查訂單 1，status 是 "已取消"

  Scenario: 已退款的訂單不能付款（邊界條件）
    Given 訂單 1 的狀態是 "已退款"
    When 店員對訂單 1 付款
    Then 回應代碼是 409，錯誤訊息是 "已退款的訂單不能付款"
    And 再查訂單 1，status 是 "已退款"

  Scenario: 訂單不存在（邊界條件）
    Given 目前沒有任何訂單
    When 店員對訂單 1 付款
    Then 回應代碼是 404，錯誤訊息是 "查無此訂單"
