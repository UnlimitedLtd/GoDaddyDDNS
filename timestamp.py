"""Functions for timestamps"""

from datetime import datetime


class TimeStamp:  # pylint: disable=too-few-public-methods
    """Static datetime related functions that can also be used as a mixin"""

    @staticmethod
    def get_timestamp():
        """Get a UTC timestamp"""
        return datetime.utcnow().strftime("[%Y-%m-%dT%H:%M:%SZ]")
