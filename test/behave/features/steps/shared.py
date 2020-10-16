from behave import *
from io import StringIO
import sys
from http_log_monitoring.log_monitor import main

@given('we capture output')
def step_impl(context):
    context.real_stdout = sys.stdout
    context.mock_stdout = StringIO()
    sys.stdout = context.mock_stdout

@when('the service reads logs "{log_file}"')
def step_impl(context, log_file):
    main(log_file, 10, False)