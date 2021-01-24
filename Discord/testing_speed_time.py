import datetime
import re


def start():
    started = datetime.datetime.now()
    return started


def stop(started):
    stopped = datetime.datetime.now()
    result_time = str(stopped - started)
    # result = re.sub(r'([^\n].*)\.([^\n].*)', r'\2', result_time)
    return result_time
