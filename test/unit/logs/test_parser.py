from http_log_monitoring.logs.parser import LogParser
import pandas as pd
from datetime import datetime
import os

HEADER = ["remotehost", "rfc931", "authuser", "date", "method", "section", "path", "protocol", "status", "bytes"]
PROJECT_ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

def test_reading_line():
    with open(os.path.join("data/small_test.txt"), "r") as log_file:
        line = LogParser.read_line(log_file)
    assert line == "remotehost,rfc931,authuser,date,request,status,bytes"


def test_parsing_data():
    with open(os.path.join("data/small_test.txt"), "r") as log_file:
        # Read past the header
        LogParser.read_line(log_file)
        line = LogParser.read_line(log_file)

    parsed_line = LogParser.parse_log(line, HEADER)
    assert parsed_line == {
        'remotehost': "10.0.0.2",
        'rfc931': "-",
        'authuser': "apache",
        'date': pd.to_datetime(
                    datetime.utcfromtimestamp(1549573860).strftime('%Y-%m-%d %H:%M:%S')
                ),
        'method': 'GET',
        'section': "api",
        'path': "user",
        'protocol': "HTTP/2.0",
        'status': 200,
        'bytes': '1234'
    }

def test_parsing_header():
    with open(os.path.join("data/small_test.txt"), "r") as log_file:
        # Read past the header
        line = LogParser.read_line(log_file)

    parsed_header = LogParser.parse_header(line)

    assert parsed_header == HEADER