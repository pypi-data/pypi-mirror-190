from logging import LogRecord
from vlogging import Formatter
from vlogging import INFO

from datetime import datetime

formatter = Formatter()

def test_formatTime_isoformat():
    record = LogRecord("vlogger", INFO, "path", 1, "Message", "args", exc_info=None)
    formatTime = formatter.formatTime(record)

    dt = datetime.fromtimestamp(record.created)
    expected = dt.isoformat(sep=" ", timespec="milliseconds")
    print(formatTime)
    assert formatTime == expected


def test_formatTime_strftime():
    datefmt = "%Y-%m-%d %H:%M:%S.%f"
    record = LogRecord("vlogger", INFO, "path", 1, "Message", "args", exc_info=None)
    formatTime = formatter.formatTime(record, datefmt)

    dt = datetime.fromtimestamp(record.created)
    expected = dt.strftime(datefmt)
    print(formatTime)
    assert formatTime == expected
