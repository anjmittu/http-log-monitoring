import argparse
import os
import sys

PROJECT_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, PROJECT_ROOT)

from http_log_monitoring.utils.input import watch
from http_log_monitoring.logs.parser import LogParser
from http_log_monitoring.logs.monitor import LogMonitor


def main(log_file_path, threshold, should_continue):
    """
    This is the main function for the HTTP log monitoring service.  This will read from the log file line by line
    and process the logs.

    :param log_file_path: The path to the log file relative to the project root.
    """
    # Read the log file one line at a time in real time
    log_file = open(os.path.join(PROJECT_ROOT, log_file_path), "r")
    # The first line of the logs should be the header, this will be used to create the LogMonitor object
    log_monitor = LogMonitor(LogParser.read_line(log_file), threshold)

    # Read and process each line
    log_line = LogParser.read_line(log_file)
    while log_line:
        log_monitor.add_log(log_line)
        log_line = LogParser.read_line(log_file)

    # Watch to see if additional lines are added, and process them
    if should_continue:
        log_lines = watch(log_file)
        for log_line in log_lines:
            log_monitor.add_log(log_line)


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='A HTTP log monitoring service')
    parser.add_argument('--file', help='the name of the log file relative to the project root',
                        default="data/sample_csv.txt")
    parser.add_argument('-t', dest='threshold', help='the threshold value to cause an steps',
                        default=10)
    parser.add_argument('-c', dest='should_continue',
                        help='This indicates that the service should continue to watch the log', action='store_true')
    args = parser.parse_args()

    main(args.file, args.threshold, args.should_continue)
