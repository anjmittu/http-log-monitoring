import pandas as pd
from http_log_monitoring.utils.database import LogDatabase


class LogDatabasePandas(LogDatabase):
    """
    This class stores the logs in a database and retrieves information about the logs.
    """
    def __init__(self, header):
        """
        This initialises the class and creates the database.

        :param header: The column names for the database.
        """
        self.database = pd.DataFrame(columns=header)
        self.database["date"] = self.database["date"].astype('datetime64[ns]')

    def add_to_db(self, loglines):
        """
        This adds a new log to the database.

        :param loglines: The log to be added.  This should be a dict with the log values.
        """
        self.database = self.database.append(loglines, ignore_index=True)

    def remove_old_logs(self, current_time):
        """
        This will remove old logs from the database who's time is greater than the MAX_HOLD_LOGS value.

        :param current_time: The current time from the last log message
        """
        self.database = self.database.loc[
            (current_time - self.database["date"]) <= LogDatabase.get_time_diff_for_alerts()
            ]

    def get_avg_num_logs(self):
        """
        This will get the average number of logs per sec in the database.
        :return: the average number of logs per sec
        """

        return int(self.database["date"].value_counts().sum()) // 120

    def get_stats(self, current_time, last_print):
        """
        This will return statistics for the logs which occurred in the time period given by STATS_TIME.
        :param current_time: The current time from the last log message
        :param last_print: The last time statistics were printed
        :return: The last time statistics were printed
        """
        logs_for_stats = self.database.loc[
            (current_time >= self.database["date"]) & (self.database["date"] > last_print)
            ]
        if len(logs_for_stats):
            section_stat = logs_for_stats["section"].value_counts().idxmax()
            user_stat = logs_for_stats["authuser"].value_counts().idxmax()
            failed_request = len(logs_for_stats.loc[logs_for_stats["status"] >= 400])
            num_logs = len(logs_for_stats)
            last_print = logs_for_stats["date"].unique().max()
            print("{}: Number of logs: {}, Top hit section: {}, Top user: {}, Failed request: {}".format(
                current_time,
                num_logs,
                section_stat,
                user_stat,
                failed_request)
            )
        return last_print

