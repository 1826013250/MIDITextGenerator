from curses import *
from functools import wraps


def safe_exception(func):
    @wraps(func)
    def wrap(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        except error as e:
            echo()
            nocbreak()
            endwin()
            print("Program encountered an error. Please check your terminal size or program settings.")
        except AssertionError as e:
            echo()
            nocbreak()
            endwin()
            raise e
    return wrap
