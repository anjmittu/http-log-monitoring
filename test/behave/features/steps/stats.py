from behave import *


@then('statistics should be printed')
def step_impl(context):
    assert "Number of logs" in context.mock_stdout.getvalue()


@then('statistics be correct')
def step_impl(context):
    assert "Number of logs: 11, Top hit section: api, Top user: apache, Failed request: 0" in context.mock_stdout.getvalue()


@then('last line is printed')
def step_impl(context):
    assert "Number of logs: 1, Top hit section: api, Top user: test, Failed request: 0" in context.mock_stdout.getvalue()
