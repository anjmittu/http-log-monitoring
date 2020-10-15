from datetime import datetime
import pandas as pd

REQUEST_PARTS = ["method", "section", "path", "protocol"]

class LogParser():
    """
    This class is used to parse log messages.
    """

    def read_line(log_file):
        """
        This will read a line from the log file.  It will remove quotes and new line charaters.
        :return: Returns a string with the log message
        """
        return log_file.readline().replace("\"", "").replace("\n", "")

    def parse_log(line, header):
        """
        This will parse a line from the log file.  It separates the log into parts based on the header
        from the log file.

        :param header: The header from the log file.
        :return: The parsed log message as a dict
        """
        line_as_dict = {}
        i = 0
        for val in line.split(","):
            if header[i] == "method":
                # The request field needs to be split in four parts
                split_request = val.split(" ")

                # The first field is the method
                line_as_dict[header[i]] = split_request[0]

                # The next two fields come from the path
                path_split = split_request[1].split("/", 2)
                line_as_dict[header[i + 1]] = path_split[1]
                if len(path_split) > 2:
                    line_as_dict[header[i + 2]] = path_split[2]
                else:
                    line_as_dict[header[i + 2]] = ""

                # The last field is the protocol
                line_as_dict[header[i + 3]] = split_request[2]

                i += len(REQUEST_PARTS)
            elif header[i] == "date":
                # The date should be turned into a datetime
                line_as_dict[header[i]] = pd.to_datetime(
                    datetime.utcfromtimestamp(int(val)).strftime('%Y-%m-%d %H:%M:%S')
                )
                i += 1
            elif header[i] == "status":
                # The status should be converted to a int
                line_as_dict[header[i]] = int(val)
                i += 1
            else:
                line_as_dict[header[i]] = val
                i += 1
        return line_as_dict

    def parse_header(header):
        """
        This will parse the header of the log file.  It will split the request field into four different columns.
        :return: a list of the column names
        """
        headers = []
        for col in header.split(","):
            if col == "request":
                headers.extend(REQUEST_PARTS)
            else:
                headers.append(col)
        return headers
