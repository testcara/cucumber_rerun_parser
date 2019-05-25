@examples
Feature: Login_1

  Scenario: Login as admin user
    Given I am a "devel" user
    When  I visit "/errata"
    Then  I can find content header "Advisories"
    And   I can find header "Advisories"
