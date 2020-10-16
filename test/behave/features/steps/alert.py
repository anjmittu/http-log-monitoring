from behave import *


@then('an alert should be thrown')
def step_impl(context):
    assert "High traffic generated" in context.mock_stdout.getvalue()

@then('an alert should recover')
def step_impl(context):
    assert "recovered" in context.mock_stdout.getvalue()