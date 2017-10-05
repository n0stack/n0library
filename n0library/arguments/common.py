from argparse import ArgumentParser
from argparse import Namespace, HelpFormatter  # NOQA
from typing import Optional, Any  # NOQA
import os

from n0library.logger import Logger


class CommonArguments(ArgumentParser):
    """Manage common arguments on n0stack

    1. Call get_common_args() before set specific arguments of proccesses
    2. Set common arguments as parents
    3. Call common_initialize() after parsed args

    Examples:
        on n0core.cmd.n0core-porter-flat like these
        ```
        argparser = CommonArguments(
            description="Process of n0stack porter type flat"
        )  # type: ArgumentParser
        argparser.add_argument("--interface-name",
                              type=str,
                              default=None,
                              help="Set interface name to create br-flat automatically")
        argparser.add_argument("--bridge-name",
                              type=str,
                              default=None,
                              help="Set bridge name of already exists like br-flat")
        args = argparser.parse_args()
        ```
    """

    def __init__(self, **kwds):
        # type: (**Any) -> None
        """Get ArgumentParser setted some common arguments.

        - Messaging queue options
        - Log options

        Returns:
            ArgumentParser prepared as one of parents.
        """
        super().__init__(**kwds)
        self.__initialized = False

        self.add_argument("--mq-url",
                          type=str,
                          default="pulsar://localhost:6650",
                          help="Set messaging queue url (Default: pulsar://localhost:6650)")
        self.add_argument("--log-no-stdout",
                          default=False,
                          action="store_true",
                          help="Disable log output for stdout")
        self.add_argument("--log-no-file",
                          default=False,
                          action="store_true",
                          help="Disable log output for file")
        self.add_argument("--log-filepath",
                          type=str,
                          default="/var/log/n0stack/{}.log".format(os.path.basename(__file__)),
                          help="Set log file path (Default: /var/log/n0stack/{}.log".format(os.path.basename(__file__)))  # NOQA
        self.add_argument("--log-level",
                          type=str,
                          choices=Logger.LEVELS,
                          default="warning",
                          help="Set log level (Default: warning)")

    def parse_args(self, *args, **kwds):
        # type: (*Any, **Any) -> Namespace
        self.__args = super().parse_args(*args, **kwds)
        self.__common_initialize()

        return self.__args

    def __common_initialize(self):
        # type: () -> None
        """Initilize with common options.

        - Initialize root logger

        Args:
            arguments: Arguments parsed by ArgumentParser within CommonParser.
        """
        if self.__initialized:
            return

        if self.__args.log_no_file:
            filepath = None  # type: Optional[str]
        else:
            filepath = self.__args.log_filepath

        Logger(name='',
               level=self.__args.log_level,
               stdout=not(self.__args.log_no_stdout),
               filepath=filepath)

        self.__initialized = True
