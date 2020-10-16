from behave import *
from http_log_monitoring.log_monitor import main
from io import StringIO
import sys

@given('we capture output')
def step_impl(context):
    context.real_stdout = sys.stdout
    context.mock_stdout = StringIO()
    sys.stdout = context.mock_stdout

@when('the service reads logs which surpass the threshold')
def step_impl(context):
    main("data/alert_test.txt", 10, False)

@then('an alert should be thrown')
def step_impl(context):
    assert "High traffic generated" in context.mock_stdout.getvalue()

@then('an alert should recover')
def step_impl(context):
    assert "recovered" in context.mock_stdout.getvalue()