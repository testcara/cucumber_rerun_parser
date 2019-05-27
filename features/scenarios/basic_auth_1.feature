@examples
Feature: Login_1

  Background:
  Given I am a "devel" user

  Scenario Outline: Login as admin user
    When  I visit "<page_name>"
    Then  I can find content header "Advisories"
    And   I can find header "Advisories"
 
  Examples:
  | page_name |
  |  errata   |
  |  bug      |
