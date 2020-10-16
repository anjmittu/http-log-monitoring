Feature: Testing that an alerts work

  Scenario: Tests that an alert is thrown
    Given we capture output
    When the service reads logs "data/alert_test.txt"
    Then an alert should be thrown


   Scenario: Tests that an alert recovery
    Given we capture output
    When the service reads logs "data/alert_test.txt"
    Then an alert should recover