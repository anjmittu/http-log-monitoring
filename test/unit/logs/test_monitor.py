from http_log_monitoring.logs.monitor import LogMonitor
import pandas as pd
from datetime import datetime

HEADER = 'remotehost,rfc931,authuser,date,request,status,bytes'


def test_time_parameters():
    monitor = LogMonitor(HEADER, 10)
    monitor.add_log("10.0.0.2,-,apache,1549573860,GET /api/user HTTP/1.0,200,1234")
    assert monitor.last_print_time == pd.to_datetime(
        datetime.utcfromtimestamp(int(1549573859)).strftime('%Y-%m-%d %H:%M:%S')
    )
    assert monitor.first_log_time == pd.to_datetime(
        datetime.utcfromtimestamp(int(1549573860)).strftime('%Y-%m-%d %H:%M:%S')
    )


def test_print_time_update():
    monitor = LogMonitor(HEADER, 10)
    monitor.add_log("10.0.0.2,-,apache,1549573860,GET /api/user HTTP/1.0,200,1234")
    monitor.add_log("10.0.0.2,-,apache,1549573870,GET /api/user HTTP/1.0,200,1234")
    assert monitor.last_print_time == pd.to_datetime(
        datetime.utcfromtimestamp(int(1549573870)).strftime('%Y-%m-%d %H:%M:%S')
    )


def test_alert_is_set():
    monitor = LogMonitor(HEADER, 10)
    monitor.add_log("10.0.0.2,-,apache,1549573860,GET /api/user HTTP/1.0,200,1234")
    for i in range(121):
        for _ in range(10):
            monitor.add_log("10.0.0.2,-,apache,{},GET /api/user HTTP/1.0,200,1234".format(1549573860+i))

    assert monitor.alert


def test_alert_is_recovers():
    monitor = LogMonitor(HEADER, 10)
    monitor.add_log("10.0.0.2,-,apache,1549573860,GET /api/user HTTP/1.0,200,1234")
    for i in range(121):
        for _ in range(10):
            monitor.add_log("10.0.0.2,-,apache,{},GET /api/user HTTP/1.0,200,1234".format(1549573860+i))

    monitor.add_log("10.0.0.2,-,apache,1549574000,GET /api/user HTTP/1.0,200,1234")

    assert not monitor.alert

