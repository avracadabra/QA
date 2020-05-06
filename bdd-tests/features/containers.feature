Feature: containers visualisation

  As user
  In order to manage containers
  I want to be able to navigate through them

  Background:
    Given I open the backend
    Ang I go to the "containers / containers" page

  Scenario: Reading results
    When page is loaded
    Then at least "2" containers are present
