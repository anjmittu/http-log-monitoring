from http_log_monitoring.logs.parser import LogParser
from http_log_monitoring.utils.database import LogDatabase
from http_log_monitoring.utils.database.pandas_db import LogDatabasePandas


class LogMonitor:
    """
    This class will monitor new logs being processed by the application.  It will print statistics on the logs and
    handle alerts.
    """
    def __init__(self, log_header, threshold):
        """
        This initialises the class.
        :param log_header: The column names for the database.
        :param threshold: The threshold value to cause an steps
        """
        self.header = LogParser.parse_header(log_header)
        self.saved_logs = LogDatabasePandas(self.header)
        self.threshold = threshold

        # These values will hold the last time statistics were printed and the time of the first log.
        self.last_print_time = None
        self.first_log_time = None

        self.alert = False

    def add_log(self, new_log_line):
        """
        This will add a new log message to the monitoring service.  It will add the log to the database and check for
        any alerts.  It will also print statistics if it is over the time to do so.  Last it will remove old logs from
        the database.

        :param new_log_line: The new log message to add
        """
        parsed_log = LogParser.parse_log(new_log_line, self.header)
        current_time = parsed_log["date"]

        # Set values when the first log comes
        if self.last_print_time is None:
            self.last_print_time = current_time
            self.first_log_time = current_time

        # Add log to db
        self.saved_logs.add_to_db(parsed_log)

        # Remove any logs greater than the max hold time
        self.saved_logs.remove_old_logs(current_time)

        # We need to have 2 mins of logs before we can check for alerts
        if (current_time - self.first_log_time) >= LogDatabase.get_time_diff_for_alerts():
            avg_logs = self.saved_logs.get_avg_num_logs()
            # If there was an steps, check if the steps is over
            if self.alert and avg_logs < self.threshold:
                # Turn the alarm off
                self.alert = False
                print("Alert has recovered at {}".format(current_time))
            # If there is not an steps, see if there should be one
            elif not self.alert and avg_logs >= self.threshold:
                # Turn on the steps
                self.alert = True
                print("High traffic generated an steps - hits = {}, triggered at {}".format(avg_logs, current_time))

        if current_time - self.last_print_time > LogDatabase.get_time_diff_for_stats():
            # Look at the last 10 seconds
            num_logs, section_stat, user_stat, failed_request = self.saved_logs.get_stats(current_time)
            print("{}: Number of logs: {}, Top hit section: {}, Top user: {}, Failed request: {}".format(
                current_time,
                num_logs,
                section_stat,
                user_stat,
                failed_request)
            )
            self.last_print_time = current_time
