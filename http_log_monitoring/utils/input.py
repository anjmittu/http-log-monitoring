import os
import time

"""
This function will match the given file for any updates.  It will return the added lines.
"""
def watch(thefile):
    thefile.seek(0, os.SEEK_END)
    while True:
        line = thefile.readline()
        if not line:
            time.sleep(1)
            continue
        yield line