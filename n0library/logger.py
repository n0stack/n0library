from typing import List, Set, Dict, Tuple, Text, Optional, Any  # NOQA
from logging import getLogger, INFO, WARNING, ERROR, DEBUG, Formatter, Logger as LoggerType  # NOQA
from logging.handlers import RotatingFileHandler as RFH
from logging import StreamHandler as SH
import sys


class Logger():
    """n0stack common logger class.

    Logger output unified log format, ltsv.

    - Set configurations on root logger.
    - Set logger name on non-root logger with root logger configurations.
    - Set propagate flag on non-root logger automaticaly when setted some configurations.

    Example:
        >>> log1 = Logger(name="", stdout=False, level="debug", filepath="./log/test/test.log")
        >>> log1.info("tester")
        - - - - - - - - - - - - - - -  -  -
        >>> log2 = Logger(__name__)
        >>> log2.info("tester")
        - - - - - - - - - - - - - - -  -  -
        >>> log3 = Logger(name="foo", stdout=False, level="debug", filepath="./log/test/test.log")
        >>> log3.info("tester")
    """

    LOGFMT = "time:%(asctime)s \t name:[%(name)s] \tseverity:[%(levelname)s] \tmessage:%(message)s  "  # type: str
    LEVELS = {"info": INFO, "warning": WARNING, "error": ERROR, "debug": DEBUG}  # type: dict

    def __init__(self, *, name=sys.argv[0], stdout=None, filepath=None, level=None):
        # type: (str, bool, str, str) -> None
        """
        Args:
            logger(str): logger name
            stdout(bool): True or False
            level(str): "info" or "warning" or "error" or "debug"
            filepath (str): fileout path

        Exceptions:
            TypeError: Log level is empty when setting root logger.
        """

        self.logger = getLogger(str(name))  # type: LoggerType

        if stdout is not None and stdout:
            stdout_handler = SH(sys.stdout)  # type: SH
            stdout_handler.setFormatter(Formatter(Logger.LOGFMT))
            stdout_handler.setLevel(Logger.LEVELS[level])
            self.logger.addHandler(stdout_handler)

            if name:
                self.logger.propagate = False

        if filepath is not None and filepath:
            file_handler = RFH(filepath, 'a+', 100000, 100)  # type: RFH
            file_handler.setFormatter(Formatter(Logger.LOGFMT))
            file_handler.level = Logger.LEVELS[level]
            self.logger.addHandler(file_handler)

            if name:
                self.logger.propagate = False

        if not level and not name:
            raise TypeError("Set log level when setting configurations on root logger")

        if level:
            self.logger.setLevel(Logger.LEVELS[level])

    def info(self, msg, extra=None):
        # type: (str, Dict[str, Any]) -> None
        self.logger.info(msg, extra=extra)

    def error(self, msg, extra=None):
        # type: (str, Dict[str, Any]) -> None
        self.logger.error(msg, extra=extra)

    def debug(self, msg, extra=None):
        # type: (str, Dict[str, Any]) -> None
        self.logger.debug(msg, extra=extra)

    def warn(self, msg, extra=None):
        # type: (str, Dict[str, Any]) -> None
        self.logger.warn(msg, extra=extra)
