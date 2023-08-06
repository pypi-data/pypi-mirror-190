import logging
import logging.config

from vlogging.logger import Logger
from vlogging.formatters import Formatter

__version__ = "0.0.1"

__all__ = ["Formatter", "Logger"]

from logging import (
    CRITICAL,
    FATAL,
    ERROR,
    WARNING,
    WARN,
    INFO,
    DEBUG,
    NOTSET,
)

SIMPLE_FORMAT = "%(asctime)s %(levelname)-8s %(message)s"
BASIC_FORMAT = "%(asctime)s %(levelname)-8s %(filename)s:%(lineno)d: %(message)s"

DATE_FMT_MICROSECONDS = "%Y-%m-%d %H:%M:%S.%f"

DEFAUT_CONFIG = {
    "version": 1,
    "disable_existing_loggers": False,
    "formatters": {
        "simple": {
            "class": "vlogging.Formatter",
            "format": SIMPLE_FORMAT,
        },
        "basic": {
            "class": "vlogging.Formatter",
            "format": BASIC_FORMAT,
            "datefmt": DATE_FMT_MICROSECONDS
        }
    },
    "handlers": {
        "consoleHandler": {
            "class": "logging.StreamHandler",
            "level": "DEBUG",
            "formatter": "basic",
            "stream": "ext://sys.stdout"
        },
    },
    "loggers": {
        "vlogger": {
            "level": "DEBUG",
            "handlers": [
                "consoleHandler"
            ]
        }
    },
    "root": {
        "level": "ERROR"
    }
}

def dictConfig(config: dict) -> None:
    """Configure logging using a dictionary.

    Parameters
    ----------
    config : dict
        config
    """
    logging.config.dictConfig(config)


def getLogger(name: str=None, config: dict=None) -> Logger:
    """
    Return a logger with the specified name, creating it if necessary.

    If no name is specified, return the root logger.

    Parameters
    ----------
    name : str, optional
        logger name, by default None
    config : dict, optional
        Configure logging using a dictionary, by default None

    Returns
    -------
    Logger
        logger
    """
    if config is not None:
        dictConfig(config)
    return logging.getLogger(name)


logging.setLoggerClass(Logger)
