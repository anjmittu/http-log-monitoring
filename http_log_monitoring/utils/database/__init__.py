import pandas as pd

# This is the maximum time the logs should be stored
# This value is set to 2 hours, since this is the longest we need to look up a log
MAX_HOLD_LOGS = 2

# This gives the time period on when statistics should be printed
# This value is set to 10 secs
STATS_TIME = 10


class LogDatabase:
    @staticmethod
    def get_time_diff_for_stats():
        """
        :return: This will return a Timedelta object with the difference given by STATS_TIME.
        """
        return pd.Timedelta(STATS_TIME, 's')

    @staticmethod
    def get_time_diff_for_alerts():
        """
                :return: This will return a Timedelta object with the difference given by MAX_HOLD_LOGS.
                """
        return pd.Timedelta(MAX_HOLD_LOGS, 'm')

    def add_to_db(self, loglines):
        """
        This adds a new log to the database.

        :param loglines: The log to be added.  This should be a dict with the log values.
        """
        pass

    def remove_old_logs(self, current_time):
        """
        This will remove old logs from the database who's time is greater than the MAX_HOLD_LOGS value.

        :param current_time: The current time from the last log message
        """
        pass

    def get_avg_num_logs(self):
        """
        This will get the average number of logs per sec in the database.
        :return: the average number of logs per sec
        """
        pass

    def get_stats(self, current_time):
        """
        This will return statistics for the logs which occurred in the time period given by STATS_TIME.
        :param current_time: The current time from the last log message
        :return: num_logs - The number of logs
                section_stat - the most frequently logged section
                user_stat - the most frequently logged user
                failed_request - the number of failed requests
        """
        pass
