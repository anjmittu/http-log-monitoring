from datetime import datetime

class LogParser():

    def read_line(log_file):
        return log_file.readline().replace("\"", "").replace("\n", "")


    def parse_log(line, header):
        line_as_dict = {}
        i = 0
        for val in line.split(","):
            if header[i] == "method":
                split_request = val.split(" ")
                for j in range(len(split_request)):
                    line_as_dict[header[i+j]] = split_request[j]
                i+=len(split_request)
            elif header[i] == "date":
                line_as_dict[header[i]] = datetime.utcfromtimestamp(int(val)).strftime('%Y-%m-%d %H:%M:%S')
                i+=1
            else:
                line_as_dict[header[i]] = val
                i+=1
        return line_as_dict

    def parse_header(header):
        headers = []
        for col in header.split(","):
            if col == "request":
                headers.extend(["method", "section", "protocol"])
            else:
                headers.append(col)
        return headers
