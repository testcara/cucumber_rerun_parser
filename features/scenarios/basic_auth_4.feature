@examples
Feature: Login_2

  Scenario: Login as project manager
    Given I am a "devel" user
    When  I open "/errata"
    Then  I cannot find content header "Advisories"
