Feature: Testing that statistics are shown correctly

  Scenario: Tests statistics are printed
    Given we capture output
    When the service reads logs "data/small_test.txt"
    Then statistics should be printed

  Scenario: Tests statistics are printed correctly
    Given we capture output
    When the service reads logs "data/small_test.txt"
    Then statistics be correct

  Scenario: Additional statistics are printed at the end
    Given we capture output
    When the service reads logs "data/small_test.txt"
    Then last line is printed
