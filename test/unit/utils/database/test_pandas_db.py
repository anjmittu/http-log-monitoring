from http_log_monitoring.utils.database.pandas_db import LogDatabasePandas
import pandas as pd
from datetime import datetime

HEADER = ["remotehost", "rfc931", "authuser", "date", "method", "section", "path", "protocol", "status", "bytes"]


def test_adding_to_db():
    db = LogDatabasePandas(HEADER)
    db.add_to_db({
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
    })

    assert db.database["remotehost"][0] == "10.0.0.2"


def test_removing_old_logs():
    db = LogDatabasePandas(HEADER)
    db.add_to_db({
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
    })
    current_time = pd.to_datetime(
        datetime.utcfromtimestamp(1549574000).strftime('%Y-%m-%d %H:%M:%S')
    )
    db.remove_old_logs(current_time)

    assert len(db.database) == 0


def test_avg_logs():
    db = LogDatabasePandas(HEADER)
    for i in range(120):
        db.add_to_db({
            'remotehost': "10.0.0.2",
            'rfc931': "-",
            'authuser': "apache",
            'date': pd.to_datetime(
                        datetime.utcfromtimestamp(1549573860+i).strftime('%Y-%m-%d %H:%M:%S')
                    ),
            'method': 'GET',
            'section': "api",
            'path': "user",
            'protocol': "HTTP/2.0",
            'status': 200,
            'bytes': '1234'
        })

    assert db.get_avg_num_logs() == 1


def test_getting_stats():
    db = LogDatabasePandas(HEADER)
    db.add_to_db({
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
    })
    current_time = pd.to_datetime(
            datetime.utcfromtimestamp(1549573920).strftime('%Y-%m-%d %H:%M:%S')
        )
    last_print = pd.to_datetime(
            datetime.utcfromtimestamp(1549573859).strftime('%Y-%m-%d %H:%M:%S')
        )
    assert db.get_stats(current_time, last_print) == pd.to_datetime(
            datetime.utcfromtimestamp(1549573860).strftime('%Y-%m-%d %H:%M:%S')
        )



