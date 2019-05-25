@examples
Feature: Login_3

  Scenario: Login as qa user
    Given I am a "devel" user
    When  I visit "/errata"
    Then  I find content header "Advisories"
