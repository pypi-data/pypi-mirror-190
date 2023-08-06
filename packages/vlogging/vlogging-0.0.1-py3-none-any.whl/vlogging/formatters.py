import logging
from datetime import datetime

class Formatter(logging.Formatter):
    """
    Formatter instances are used to convert a LogRecord to text.

    %(name)s            Name of the logger (logging channel)
    %(levelno)s         Numeric logging level for the message (DEBUG, INFO,
                        WARNING, ERROR, CRITICAL)
    %(levelname)s       Text logging level for the message ("DEBUG", "INFO",
                        "WARNING", "ERROR", "CRITICAL")
    %(pathname)s        Full pathname of the source file where the logging
                        call was issued (if available)
    %(filename)s        Filename portion of pathname
    %(module)s          Module (name portion of filename)
    %(lineno)d          Source line number where the logging call was issued
                        (if available)
    %(funcName)s        Function name
    %(created)f         Time when the LogRecord was created (time.time()
                        return value)
    %(asctime)s         Textual time when the LogRecord was created
    %(msecs)d           Millisecond portion of the creation time
    %(relativeCreated)d Time in milliseconds when the LogRecord was created,
                        relative to the time the logging module was loaded
                        (typically at application startup time)
    %(thread)d          Thread ID (if available)
    %(threadName)s      Thread name (if available)
    %(process)d         Process ID (if available)
    %(processName)s     Process name (if available)
    %(message)s         The result of record.getMessage(), computed just as
                        the record is emitted
    """

    def formatTime(self, record: logging.LogRecord, datefmt: str=None) -> str:
        """
        Return the creation time of the specified LogRecord as formatted text.

        Parameters
        ----------
        record : logging.LogRecord
            log record
        datefmt : str, optional
            datetime format, by default None

        Returns
        -------
        str
            formatted text
        """
        dt = datetime.fromtimestamp(record.created)
        if datefmt is None:
            time = dt.isoformat(sep=" ", timespec="milliseconds")
        else:
            time = dt.strftime(datefmt)
        return time
