import sys


LOCALHOST = True


def init() -> None:
    global LOCALHOST
    LOCALHOST = True if sys.platform == 'win32' or (len(sys.argv) > 1 and sys.argv[-1] == '--local') else False


def set_local() -> None:
    global LOCALHOST
    LOCALHOST = True
