Feature: Amazon India search
  In order to find products
  As a shopper
  I want to search on Amazon India

  Scenario: Search for iPhone and sort by price
    Given I open Amazon India homepage
    When I search for "Iphone 17 pro max"
    And I sort results by price low to high
    Then I should see search results sorted by price low to high
