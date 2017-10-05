import sys
from typing import Union, Dict, Optional, Any  # NOQA

from logging import getLogger, Formatter
from logging import INFO, WARNING, ERROR, DEBUG
from logging import StreamHandler as SH
from logging.handlers import RotatingFileHandler as RFH


class Logger():
    """n0stack common logger class.

    Logger output logs with unified format, ltsv.

    Usecases:
        - Set configurations on root logger.
        - Set logger name on non-root logger with root logger configurations.
        - Set propagate flag on non-root logger automaticaly when setted some configurations.

    Example:
        >>> log1 = Logger(name="", stdout=True, level="debug", filepath="log/log1.log")
        >>> log1.info("hoge")
        time:2017-10-05 01:42:14,078     name:root      severity:INFO   message:hoge
        - - - - - - - - - - - - - - -  -  -
        >>> log2 = Logger(__name__)
        >>> log2.info("tester")
        time:2017-10-05 01:45:00,402     name:__main__  severity:INFO   message:foo
        - - - - - - - - - - - - - - -  -  -
        >>> log3 = Logger(name="log3", stdout=True, level="debug", filepath="log/log2.log")
        >>> log3.info("tester")
        time:2017-10-05 01:45:52,066     name:log3      severity:INFO   message:bar
    """

    LOGFMT = "time:%(asctime)s \t name:%(name)s \tseverity:%(levelname)s \tmessage:%(message)s"  # type: str
    LEVELS = {"info": INFO, "warning": WARNING, "error": ERROR, "debug": DEBUG}  # type: Dict[str, int]

    def __init__(self,
                 name=sys.argv[0],  # type: Optional[str]
                 *,
                 stdout=None,  # type: Optional[bool]
                 filepath=None,  # type: Optional[str]
                 level='',  # type: str
                 propagate=False  # type: bool
                 ):
        # type: (...) -> None
        """
        Args:
            name: Set Logger name. When you want to use root logger, set None.
            stdout: Set True when needing stdout.
            filepath: Set file path to output logs.
            level: Choose from `Logger.LEVELS`.
            propagate: Set logger.propagate when some configurations setted.

        Exceptions:
            TypeError: Log level is empty when setting some configurations,
                       because empty level would make bug.
        """

        self._logger = getLogger(str(name))

        if not level and (stdout or filepath):
            raise TypeError("Set log level when setting some configurations")
        elif level:
            self._logger.setLevel(self.LEVELS[level])
            self._logger.propagate = propagate

        if stdout is not None and stdout:
            stdout_handler = SH(sys.stdout)
            stdout_handler.setFormatter(Formatter(self.LOGFMT))
            stdout_handler.setLevel(self.LEVELS[level])
            self._logger.addHandler(stdout_handler)
            self._logger.propagate = propagate

        if filepath is not None and filepath:
            file_handler = RFH(filepath, 'a+', 100000, 100)
            file_handler.setFormatter(Formatter(self.LOGFMT))
            file_handler.level = self.LEVELS[level]
            self._logger.addHandler(file_handler)
            self._logger.propagate = propagate

    def info(self, msg, extra=None):
        # type: (str, Optional[Dict[str, Any]]) -> None
        self._logger.info(msg, extra=extra)

    def error(self, msg, extra=None):
        # type: (str, Optional[Dict[str, Any]]) -> None
        self._logger.error(msg, extra=extra)

    def debug(self, msg, extra=None):
        # type: (str, Optional[Dict[str, Any]]) -> None
        self._logger.debug(msg, extra=extra)

    def warning(self, msg, extra=None):
        # type: (str, Optional[Dict[str, Any]]) -> None
        self._logger.warning(msg, extra=extra)
