from typing import List, Set, Dict, Tuple, Text, Optional, Any  # NOQA
from logging import getLogger, INFO, WARNING, ERROR, DEBUG, Formatter, Logger as LoggerType  # NOQA
from logging.handlers import RotatingFileHandler as RFH
from logging import StreamHandler as SH
import sys


class Logger():
    LOGFMT = "time:%(asctime)s \t name:[%(name)s] \tseverity:[%(levelname)s] \tmessage:%(message)s  "  # type: str
    LEVELS = {"info": INFO, "warning": WARNING, "error": ERROR, "debug": DEBUG}  # type: dict

    def __init__(self, *, name=sys.argv[0], stdout=True, level="debug", filepath=None):
        # type: (str, bool, str, str) -> None
        """
        Args:
            logger(str): logger name
            stdout(bool): True or False
            level(str): "info" or "warning" or "error" or "debug"
            filepath (str): fileout path

        Example:
            >>> from n0library.logger import Logger
            >>> log = Logger()
            >>> log.info("tester")
            - - - - - - - - - - - - - - -  -  -
            >>> from n0library.logger import Logger
            >>> log = Logger(name="test", stdout=False, level="debug", filepath="./log/test/test.log")
            >>> log.info("tester")
        """

        self.logger = getLogger(str(name))  # type: LoggerType

        if stdout:
            stdout_handler = SH(sys.stdout)  # type: SH
            stdout_handler.setFormatter(Formatter(Logger.LOGFMT))
            stdout_handler.setLevel(Logger.LEVELS[level])
            self.logger.addHandler(stdout_handler)

        if filepath is not None:
            file_handler = RFH(filepath, 'a+', 100000, 100)  # type: RFH
            file_handler.setFormatter(Formatter(Logger.LOGFMT))
            file_handler.level = Logger.LEVELS[level]
            self.logger.addHandler(file_handler)

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
