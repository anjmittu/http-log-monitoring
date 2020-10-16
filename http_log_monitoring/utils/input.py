import os
import time
from http_log_monitoring.logs.parser import LogParser

def watch(log_file):
    """
    This function will watch the given file for any updates.

    :param the_file: The file to watch
    :return: Added file lines.
    """
    log_file.seek(0, os.SEEK_END)
    while True:
        line = LogParser.read_line(log_file)
        if not line:
            time.sleep(1)
            continue
        yield line