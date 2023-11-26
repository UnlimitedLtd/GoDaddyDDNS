"""Handy utilities"""

from datetime import datetime


def timestamp():
    """Get a UTC timestamp"""
    return datetime.utcnow().strftime("[%Y-%m-%dT%H:%M:%SZ]")


class Verbose:  # pylint: disable=too-few-public-methods
    """Provides functions for verbose printing"""

    def __init__(self, verbose: bool = False):
        self.verbose = verbose

    def printer(self, message: str) -> None:
        """Prints is verbose is True

        :param message: The message to print
        """
        if self.verbose:
            print(timestamp(), message)
