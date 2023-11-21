"""Functions for timestamps"""

from datetime import datetime


def get_timestamp():
    """Get a UTC timestamp"""
    return datetime.utcnow().strftime("[%Y-%m-%dT%H:%M:%SZ]")
