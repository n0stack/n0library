from logging import getLogger, INFO, WARNING, ERROR, DEBUG, Formatter
from logging.handlers import RotatingFileHandler as RFH
from logging import StreamHandler as SH
from datetime import datetime
import socket
import sys


class LogInit():

    def __init__(self, filepath, filename, level, stdout, fileout):
        # type: (str, str, str, bool, bool) -> None
        """
        Args:
            path (str): fileout path
            name(str): filename
            level(str): "info" or "warning" or "error" or "debug"
            stdout(bool): True or False
            fileout(bool): True or False

        Example:
            >>> from n0library.n0corelog import LogInit
            >>> log = LogInit("./log/test/", "test.log", "debug", True, True).logger
            >>> log.info("tester")
        """
        self.logger = getLogger(__name__)
        times = str(datetime.now().strftime("%Y:%m:%d-%H:%M:%S"))
        host = socket.gethostname()
        log_fmt = "time:%(asctime)s \tseverity:[%(levelname)s] \tmessage:%(message)s  "
        levels = {"info": INFO, "warning": WARNING, "error": ERROR, "debug": DEBUG}
        if(stdout):
            stdout_handler = SH(sys.stdout)
            stdout_handler.setFormatter(Formatter(log_fmt))
            stdout_handler.setLevel(levels[level])
            self.logger.addHandler(stdout_handler)
        if(fileout):
            file_handler = RFH(filepath + host + "-" + times + "-" + filename, 'a+', 100000, 100)
            file_handler.setFormatter(Formatter(log_fmt))
            file_handler.level = levels[level]
            self.logger.addHandler(file_handler)
        self.logger.setLevel(levels[level])
        self.logger.debug('Init')
