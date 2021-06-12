import sys
import traceback
import functools


def log_crash(function):
    """
    Decorator to log exceptions and stop program execution.
    """

    @functools.wraps(function)
    def wrapper(*args, **kwargs):
        try:
            return function(*args, **kwargs)
        except:
            exc_type, exc_value, exc_traceback = sys.exc_info()
            print(
                f"{function.__name__} crashed:\n "
                f"{''.join(traceback.format_tb(exc_traceback))}\n "
                f"{exc_type.__name__}:{exc_value}"
            )
            exit(1)

    return wrapper
