Feature: 查訂單

  Scenario: 編號存在，回傳整筆訂單
    Given 已新增一筆訂單：商品 "咖啡"、數量 2、單價 80
    When 店員查編號 1
    Then 拿回的訂單和新增時拿回的完全相同

  Scenario: 編號不存在，回傳 None（邊界條件）
    Given 目前已有 2 筆訂單
    When 店員查編號 99
    Then 拿回 None

  Scenario: 一筆訂單都沒有，回傳 None（邊界條件）
    Given 目前沒有任何訂單
    When 店員查編號 1
    Then 拿回 None
