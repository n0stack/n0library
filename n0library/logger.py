from logging import getLogger, INFO, WARNING, ERROR, DEBUG, Formatter
from logging.handlers import RotatingFileHandler as RFH
from logging import StreamHandler as SH
from datetime import datetime
import socket
import sys


class Logger(object):
    Logfmt = "time:%(asctime)s \tseverity:[%(levelname)s] \tmessage:%(message)s  "
    Levels = {"info": INFO, "warning": WARNING, "error": ERROR, "debug": DEBUG}

    def __init__(self, stdout, fileout, name='root', **kwargs):
        # type: (str, bool, bool, **str) -> None
        """
        Args:
            stdout(bool): True or False
            fileout(bool): True or False
            filepath (str): fileout path
            filename(str): filename
            level(str): "info" or "warning" or "error" or "debug"

        Example:
            >>> from n0library.logger import Logger
            >>> log = Logger(True, True, 'test', filepath="./log/test/", filename="test.log", level="debug").logger
            >>> log.info("tester")
        """
        self.logger = getLogger(name)
        times = str(datetime.now().strftime("%Y:%m:%d-%H:%M:%S"))
        host = socket.gethostname()

        if(stdout):
            stdout_handler = SH(sys.stdout)
            stdout_handler.setFormatter(Formatter(Logger.Logfmt))
            stdout_handler.setLevel(Logger.Levels[kwargs["level"]])
            self.logger.addHandler(stdout_handler)
        if(fileout):
            file_handler = RFH(kwargs["filepath"] + host + "-" + times + "-" + kwargs["filename"], 'a+', 100000, 100)
            file_handler.setFormatter(Formatter(Logger.Logfmt))
            file_handler.level = Logger.Levels[kwargs["level"]]
            self.logger.addHandler(file_handler)
        self.logger.setLevel(Logger.Levels[kwargs["level"]])
        self.logger.debug('Init')
