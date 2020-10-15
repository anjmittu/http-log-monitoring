import pandas as pd

# This is the maximum time the logs should be stored
# This value is set to 2 hours, since this is the longest we need to look up a log
MAX_HOLD_LOGS = 2

# This gives the time period on when statistics should be printed
# This value is set to 10 secs
STATS_TIME = 10


class LogDatabase:
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
        This adds a new logs to the database.

        :param loglines: The logs to be added.  This should be a list with a dict for each log.
        """
        self.database = self.database.append(loglines)

    def remove_old_logs(self, current_time):
        """
        This will remove old logs from the database who's time is greater than the MAX_HOLD_LOGS value.

        :param current_time: The current time from the last log message
        """
        self.database = self.database.loc[
            (current_time - self.database["date"]) < pd.Timedelta(MAX_HOLD_LOGS, 'm')
            ]

    def get_avg_num_logs(self):
        """
        This will get the average number of logs per sec in the database.
        :return: the average number of logs per sec
        """
        return int(self.database["date"].value_counts().mean())

    def get_stats(self, current_time):
        """
        This will return statistics for the logs which occurred in the time period given by STATS_TIME.
        :param current_time: The current time from the last log message
        :return: num_logs - The number of logs
                section_stat - the most frequently logged section
                user_stat - the most frequently logged user
                failed_request - the number of failed requests
        """
        logs_for_stats = self.database.loc[
            (current_time - self.database["date"]) < pd.Timedelta(STATS_TIME, 's')
            ]
        section_stat = logs_for_stats["section"].value_counts().idxmax()
        user_stat = logs_for_stats["authuser"].value_counts().idxmax()
        failed_request = len(logs_for_stats.loc[logs_for_stats["status"] >= 400])
        num_logs = len(logs_for_stats)
        return num_logs, section_stat, user_stat, failed_request

    @staticmethod
    def get_time_diff_stats():
        """
        :return: This will return a Timedelta object with the difference given by STATS_TIME.
        """
        return pd.Timedelta(STATS_TIME, 's')