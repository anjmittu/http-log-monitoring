# HTTP Log Monitoring

## How to run
This service can be run with docker or on it's own.

### Running with Docker
```
docker build -t log_monitor .
docker run -it --rm -v `pwd`:/usr/src/myapp -w /usr/src/myapp anjmittu/log_monitor python http_log_monitoring/log_monitor.py
```
