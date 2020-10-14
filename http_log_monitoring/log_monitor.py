#!/usr/bin/env python
import argparse
import os
from utils.input import watch
from logs.parser import LogParser
from logs.monitor import LogMonitor

PROJECT_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

def main(file):
    # Read the log file one line at a time in real time
    log_file = open(os.path.join(PROJECT_ROOT, file), "r")
    # The first line of the logs should be the header, this will be used to create the LogMonitor object
    log_monitor = LogMonitor(LogParser.read_line(log_file))

    # Read and process each line
    log_line = LogParser.read_line(log_file)
    while log_line:
        log_monitor.add_log(log_line)
        log_line = LogParser.read_line(log_file)

    # Watch to see if additional lines are added, and process them
    log_lines = watch(log_file)
    for log_line in log_lines:
        print(log_line)

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description = 'A HTTP log monitoring service')
    parser.add_argument('--file', help='the name of the log file', default="data/sample_csv.txt")
    args = parser.parse_args()

    main(args.file)