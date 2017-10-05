from argparse import ArgumentParser
from argparse import Namespace  # NOQA
from typing import Optional  # NOQA

from n0library.logger import Logger


class CommonArguments(object):
    """Manage common arguments on n0stack

    1. Call get_common_args() before set specific arguments of proccesses
    2. Set common arguments as parents
    3. Call common_initialize() after parsed args

    Examples:
        on n0core.cmd.n0core-porter-flat

        ```
        ca = CommonArguments()
        common_args = ca.get_common_args()
        argparser = ArgumentParser(
            description="Process of n0stack porter type flat",
            parents=[common_args]
        )  # type: ArgumentParser
        argparser.add_argument("--interface-name",
                               type=str,
                               default=None,
                               help="Set interface name to create br-flat automatically")
        argparser.add_argument("--bridge-name",
                               type=str,
                               default=None,
                               help="Set bridge name of already exists like br-flat")
        args = argparser.parse_args()  # type: Namespace
        ca.common_initialize(args)
        ```

    ToDo:
        Think whether using decorator or not.
    """

    @classmethod
    def get_common_args(cls):
        # type: () -> ArgumentParser
        """Get ArgumentParser setted some common arguments.

        - Messaging queue options
        - Log options

        Returns:
            ArgumentParser prepared as one of parents.
        """
        args = ArgumentParser(add_help=False)
        args.add_argument("--mq-url",
                          type=str,
                          default="pulsar://localhost:6650",
                          help="Set messaging queue url (Default: pulsar://localhost:6650)")
        args.add_argument("--log-no-stdout",
                          default=False,
                          action="store_true",
                          help="Disable log output for stdout")
        args.add_argument("--log-no-file",
                          default=False,
                          action="store_true",
                          help="Disable log output for file")
        args.add_argument("--log-filepath",
                          type=str,
                          default="/var/log/n0stack/n0core/porter-flat.log",
                          help="Set log file path (Default: /var/log/n0stack/n0core/porter-flat.log)")  # NOQA
        args.add_argument("--log-level",
                          type=str,
                          choices=Logger.LEVELS,
                          default="waring",
                          help="Set log level (Default: warning)")
        return args

    @classmethod
    def common_initialize(cls, arguments):
        # type: (Namespace) -> None
        """Initilize with common options.

        - Initialize root logger

        Args:
            arguments: Arguments parsed by ArgumentParser within CommonParser.
        """
        if arguments.log_no_file:
            filepath = None  # type: Optional[str]
        else:
            filepath = arguments.log_filepath

        Logger(name='',
               level=arguments.log_level,
               stdout=not(arguments.log_no_stdout),
               filepath=filepath)
