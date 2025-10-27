Feature: Example Feature
  As a developer
  I want to test the application
  So that I can verify it works correctly

  Scenario: Check application health
    Given the application is running
    When I check the health endpoint
    Then the response status should be 200
    And the response should contain "healthy"

