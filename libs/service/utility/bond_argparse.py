from libs.config import config
from argparse import ArgumentParser, RawTextHelpFormatter, ArgumentTypeError


class Args:
    def __init__(self) -> None:
        self.parser = ArgumentParser(
            description="The Bond-Agent command line tool",
            formatter_class=RawTextHelpFormatter,
        )

    def str_to_bool(self, value: str) -> bool:
        """
        Create str_to_bool function.

        :param value: [str] input value
        :return: [bool] boolean value
        """

        if isinstance(value, bool):
            return value
        elif value.lower() in ("true", "t"):
            return True
        elif value.lower() in ("false", "f"):
            return False
        else:
            raise ArgumentTypeError(f"Invalid boolean value: {value}")

    def debug_controller(self) -> None:
        """
        Add debug args controller.
        """

        self.parser.add_argument(
            "-d5",
            "--debug",
            default=False,
            help="debug function switch (default: False, you can use t/T/f/F/True/true/False/false to input)",
        )

        args = self.parser.parse_args()
        config.DEBUG = self.str_to_bool(args.debug)
