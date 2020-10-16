from http_log_monitoring.logs.parser import LogParser
from http_log_monitoring.utils.database import LogDatabase
from http_log_monitoring.utils.database.pandas_db import LogDatabasePandas
import pandas as pd


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

        self.current_time = None

        self.alert = False

    def add_log(self, new_log_line):
        """
        This will add a new log message to the monitoring service.  It will add the log to the database and check for
        any alerts.  It will also print statistics if it is over the time to do so.  Last it will remove old logs from
        the database.

        :param new_log_line: The new log message to add
        """
        parsed_log = LogParser.parse_log(new_log_line, self.header)
        self.current_time = parsed_log["date"]

        # Set values when the first log comes
        if self.last_print_time is None:
            self.last_print_time = self.current_time - pd.Timedelta(1, 's')
            self.first_log_time = self.current_time

        # Add log to db
        self.saved_logs.add_to_db(parsed_log)

        if self.current_time - self.last_print_time > LogDatabase.get_time_diff_for_stats():
            self.print_stats()

        # Remove any logs greater than the max hold time
        self.saved_logs.remove_old_logs(self.current_time)

        # We need to have 2 mins of logs before we can check for alerts
        if (self.current_time - self.first_log_time) >= LogDatabase.get_time_diff_for_alerts():
            avg_logs = self.saved_logs.get_avg_num_logs()
            # If there was an alert, check if the alert is over
            if self.alert and avg_logs < self.threshold:
                # Turn the alarm off
                self.alert = False
                print("Alert has recovered at {}".format(self.current_time))
            # If there is not an alert, see if there should be one
            elif not self.alert and avg_logs >= self.threshold:
                # Turn on the alert
                self.alert = True
                print(
                    "High traffic generated an steps - hits = {}, triggered at {}".format(avg_logs, self.current_time))

    def print_stats(self):
        # Look at the last 10 seconds
        self.last_print_time = self.saved_logs.get_stats(self.current_time, self.last_print_time)
