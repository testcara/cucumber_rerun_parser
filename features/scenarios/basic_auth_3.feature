@examples
Feature: Login_2

  Scenario: Login as devel user
    Given I am a "devel" user
    When  I visit "/errata"
    Then  I can find content header "Advisories"
