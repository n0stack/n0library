from typing import List, Set, Dict, Tuple, Text, Optional, Any  # NOQA
from logging import getLogger, INFO, WARNING, ERROR, DEBUG, Formatter, Logger as LoggerType  # NOQA
from logging.handlers import RotatingFileHandler as RFH
from logging import StreamHandler as SH
from datetime import datetime
import socket
import sys


class Logger():
    Logfmt = "time:%(asctime)s \tseverity:[%(levelname)s] \tmessage:%(message)s  "  # type: str
    Levels = {"info": INFO, "warning": WARNING, "error": ERROR, "debug": DEBUG}  # type: dict

    def __init__(self, name='', stdout=False, level="debug", **kwargs):
        # type: (str, bool, str, **str) -> None
        """
        Args:
            logger(str): logger name
            stdout(bool): True or False
            level(str): "info" or "warning" or "error" or "debug"
            filepath (str): fileout path
            filename(str): filename

        Example:
            >>> from n0library.logger import Logger
            >>> log = Logger('test', True, filepath="./log/test/", filename="test.log", level="debug")
            >>> log.info("tester")
        """
        self.logger = getLogger(name)  # type: LoggerType
        times = str(datetime.now().strftime("%Y:%m:%d-%H:%M:%S"))  # type: str
        host = socket.gethostname()  # type: str

        if(stdout):
            stdout_handler = SH(sys.stdout)  # type: SH
            stdout_handler.setFormatter(Formatter(Logger.Logfmt))
            stdout_handler.setLevel(Logger.Levels[level])
            self.logger.addHandler(stdout_handler)

        if("filepath" in kwargs):
            file_handler = RFH(kwargs["filepath"] + host + "-" + times + "-" + kwargs["filename"], 'a+', 100000, 100)  # type: RFH
            file_handler.setFormatter(Formatter(Logger.Logfmt))
            file_handler.level = Logger.Levels[level]
            self.logger.addHandler(file_handler)

        self.logger.setLevel(Logger.Levels[level])
        self.logger.debug('Init')

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
