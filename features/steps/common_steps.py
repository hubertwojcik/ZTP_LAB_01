"""
Common step definitions for Behave tests.
"""
from behave import given, when, then
import requests


@given('the application is running')
def step_application_running(context):
    """Verify application is running."""
    # This is a placeholder - implement actual check if needed
    pass


@when('I check the health                                            endpoint')
def step_check_health(context):
    """Send request to health endpoint."""
    try:
        context.response = requests.get(f"{context.base_url}/health")
    except requests.exceptions.ConnectionError:
        context.response = None
        context.error = "Connection refused"


@then('the response status should be {status_code:d}')
def step_check_status(context, status_code):
    """Verify response status code."""
    assert context.response is not None, f"Expected response but got: {context.error}"
    assert context.response.status_code == status_code, \
        f"Expected status {status_code}, got {context.response.status_code}"


@then('the response should contain "{text}"')
def step_check_response_content(context, text):
    """Verify response contains specified text."""
    assert text in context.response.text or text in str(context.response.json()), \
        f"Response does not contain '{text}'"

