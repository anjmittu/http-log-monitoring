import pandas as pd
from logs.parser import LogParser

class LogMonitor():
    def __init__(self, log_header):
        self.header = LogParser.parse_header(log_header)
        self.saved_logs = pd.DataFrame(columns=self.header)
        self.saved_logs["date"] = self.saved_logs["date"].astype('datetime64[ns]')


    def add_log(self, new_log_line):
        parsed_log = LogParser.parse_log(new_log_line, self.header)
        self.saved_logs = self.saved_logs.append(parsed_log, ignore_index=True)
        current_time = parsed_log["date"]

        # Look at the last 10 seconds
        
