Feature: Testing that an alerts work

  Scenario: Tests that an alert is thrown
    Given we capture output
    When the service reads logs which surpass the threshold
    Then an alert should be thrown


   Scenario: Tests that an alert recovery
    Given we capture output
    When the service reads logs which surpass the threshold
    Then an alert should recover