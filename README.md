# HTTP Log Monitoring

This service will intake a CSV-encoded HTTP log file and will
monitor the logs.  Every 10 secs it will print statistics on
the logs it read.  It will also set an alert any time the
logs exceed a threshold value on average for 2 minutes.
By default this value to set to 10, but can be configured.

## Overview
This service will intake a CSV-encoded HTTP log file and will
monitor the logs.  Using the `-c` parameter, the service can
be set to run continuously.  This means the program will
continue to run after reading all the data in the file, and 
will continue to process any new logs which are written to
the file.

The inputted file must have a header detailing the name of
each column.  It should have all of the following columns,
given in any order:  
`"remotehost","rfc931","authuser","date","request","status","bytes"`

Every 10 secs, statistics are printed about the logs.  These
statistics include:
- The time
- The numbers of logs read in the past 10 secs
- The top hit section
- The uses with the most hits
- The number of failed request

An example of this is: `2019-02-07 21:13:00: Number of logs: 1, Top hit section: api, Top user: apache, Failed request: 0`

The service will start an alert when the number of logs exceeds
a threshold value on average for more than 2 minutes.  By 
default this value to set to 10, but can be configured.  The
alert will give the average number logs in the past 2 
minutes and the time the allert was triggered.  When the traffic
returns to below the threshold value, the alert will recover
and a another message showing the recovery time will be 
printed.

### Directory Structure
```
- http_log_monitoring
    - logs
        - monitor.py        :- Monitor new logs being processed by the application
        - parser.py         :- Parses log messages
    - utils
        - database
            - __init__.py   :- Base LogDatabase class
            - pandas_db.py  :- Stores the logs in a pandas database
        - input.py          :- Utility functions for readin input
    - log_monitor.py        :- The main function for the HTTP log monitoring service
```

## How to run
This service can be run with docker or on it's own.  The main
program is `http_log_monitoring/log_monitor.py`.  Information
about the program parameters can be found by running
`http_log_monitoring/log_monitor.py --help`

```
usage: log_monitor.py [-h] [--file FILE] [-t THRESHOLD] [-c]

A HTTP log monitoring service

optional arguments:
  -h, --help    show this help message and exit
  --file FILE   the name of the log file relative to the project root
  -t THRESHOLD  the threshold value to cause an steps
  -c            This indicates that the service should continue to watch the log
```

With no parameters the program will run with the default 
values.  These values are given below.

```
file        :- data/sample_csv.txt
threshold   :- 10
```

### Running with Docker
#### Set up
Before running the service, docker must be installed on the
computer.  Then the docker image must be built.
```
docker build -t log_monitor .
```

After the image is built once, the program can be run with
the following command.  Optional arguments can be added
to change the default parameters of the service.

```
docker run -it --rm -v `pwd`:/usr/src/myapp -w /usr/src/myapp log_monitor python http_log_monitoring/log_monitor.py
```

Tests can be run with
```
docker run -it --rm -v `pwd`:/usr/src/myapp -w /usr/src/myapp log_monitor behave test/behave/features
```

### Running without docker
Before running the service, python3 must be installed.  
After python is installed the needed libraries can be 
installed with the following command
```
pip install -r requirements.txt
```

After these are installed, the program can be run with
the following command.  Optional arguments can be added
to change the default parameters of the service.
```
python http_log_monitoring/log_monitor.py
```

Tests can be run with
```
behave test/behave/features
```

## Implementation
Log messages are in in one line at a time.  The log is parsed,
then stored in a pandas dataframe.  The dataframe will only
hold the past 2 minutes worth of logs.  Any queries for 
statistics or alerts will be done on this dataframe.  This
allows for efficient queries over the logs.

### Improvements
I would first improve this by using a different database
library.  Pandas is efficient for the queries for alerts
and statistics, however, it is slow to add data.  Another
in-memory database could be used, such as Pyspark or 
in-memory sqlite3.  

If this service needs to be scaled
out to handle much larger amounts of data, out of memory 
databases can be used, such as MySQL or PostgreSQL. 
New databases can easily be added by extending the 
LogDatabase class.  In this way, you could have
multiple instances of this service reading from different
files, but saving to the same database.

This service could also be changed to output the information
in a format which could be more easily read by another
program.  For example, in a CSV format.

Given more time, I would have written more tests.  I would 
add additional behavior tests, to check if the statistics
are displayed correctly.  I would also add unit tests to 
test the functions in this service.


