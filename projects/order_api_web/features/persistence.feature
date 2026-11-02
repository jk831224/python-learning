Feature: 永久保存

  Scenario: 重新啟動後，訂單還在
    Given 店員已新增訂單：商品 "咖啡"、數量 2、單價 80
    When API 程式重新啟動
    And 店員查訂單 1
    Then 回應代碼是 200
    And 拿回的訂單是 id 1、商品 "咖啡"、數量 2、單價 80、total 160、shipping 60、amount_due 220、status "待付款"

  Scenario: 重新啟動後，狀態也還在（邊界條件）
    Given 店員已新增訂單：商品 "咖啡"、數量 2、單價 80
    And 店員對訂單 1 付款
    When API 程式重新啟動
    And 店員查訂單 1
    Then 拿回的訂單 status 是 "已付款"

  Scenario: 重新啟動後，編號接續，不會從 1 重來（邊界條件）
    Given 目前已有 2 筆訂單
    When API 程式重新啟動
    And 店員送出新增訂單：商品 "蛋糕"、數量 1、單價 120
    Then 拿回的訂單 id 是 3
