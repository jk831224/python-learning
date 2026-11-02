Feature: 取消

  Scenario: 待付款的訂單取消
    Given 訂單 1 的狀態是 "待付款"
    When 店員取消訂單 1
    Then 回應代碼是 200
    And 拿回的訂單 status 是 "已取消"
    And 再查訂單 1，status 是 "已取消"

  Scenario: 已付款的訂單取消，變成已退款
    Given 訂單 1 的狀態是 "已付款"
    When 店員取消訂單 1
    Then 回應代碼是 200
    And 拿回的訂單 status 是 "已退款"
    And 再查訂單 1，status 是 "已退款"

  Scenario: 已取消的訂單不能再取消（邊界條件）
    Given 訂單 1 的狀態是 "已取消"
    When 店員取消訂單 1
    Then 回應代碼是 409，錯誤訊息是 "已取消的訂單不能取消"
    And 再查訂單 1，status 是 "已取消"

  Scenario: 已退款的訂單不能取消（邊界條件）
    Given 訂單 1 的狀態是 "已退款"
    When 店員取消訂單 1
    Then 回應代碼是 409，錯誤訊息是 "已退款的訂單不能取消"
    And 再查訂單 1，status 是 "已退款"

  Scenario: 訂單不存在（邊界條件）
    Given 目前沒有任何訂單
    When 店員取消訂單 1
    Then 回應代碼是 404，錯誤訊息是 "查無此訂單"
