import logging
from logging.handlers import TimedRotatingFileHandler
from pathlib import Path

from configs.config import MainSettings
from utils.arg_parse import LOCALHOST


FORMATTER_BASIC = '%(asctime)s.%(msecs)d - %(name)s - %(levelname)s - %(message)s'
FORMATTER = logging.Formatter(
        fmt='%(asctime)s -%(name)s-%(levelname)s- %(message)s',
        datefmt='%Y.%m.%d %H:%M:%S'
        )
FORMATTER_SHORT = logging.Formatter(
        fmt='%(asctime)s -%(levelname)s- %(message)s',
        datefmt='%Y.%m.%d %H:%M:%S'
        )
FORMATTER_ERR = logging.Formatter(
        fmt='%(asctime)s.%(msecs)d - %(name)s - %(levelname)s - %(message)s',
        datefmt='%Y.%m.%d %H:%M:%S'
        )
# уровень лога NOTSET=0, DEBUG=10, INFO=20, WARNING=30, ERROR=40 и CRITICAL=50


def get_console_handler(_format: logging.Formatter = FORMATTER) -> logging.StreamHandler:
    console_handler = logging.StreamHandler()
    console_handler.setFormatter(_format)
    return console_handler


def get_file_handler(
                     filename: Path,
                     mode: str = 'a',
                     encoding: str = 'utf-8',
                     delay: bool = False,
                     _format: logging.Formatter = FORMATTER
                     ) -> logging.FileHandler:
    file_handler = logging.FileHandler(filename, mode=mode, encoding=encoding, delay=delay)
    file_handler.setFormatter(_format)
    return file_handler


def get_rotating_file_handler(
                              filename: Path,
                              mode: str = 'a',
                              max_bytes: int = 1048576,
                              backup_count: int = 3,
                              delay: bool = False,
                              _format: logging.Formatter = FORMATTER
                              ) -> TimedRotatingFileHandler:
    file_handler = TimedRotatingFileHandler(  # noqa: F821
                    filename,
                    mode,
                    maxBytes=max_bytes,
                    backupCount=backup_count,
                    delay=delay
                    )
    file_handler.setFormatter(_format)
    return file_handler


def get_timed_rotating_file_handler(
                                    filename: Path,
                                    when='midnight',
                                    backup_count=3,
                                    delay=False,
                                    _format: logging.Formatter = FORMATTER
                                    ) -> TimedRotatingFileHandler:
    file_handler = TimedRotatingFileHandler(
                    filename,
                    when=when,
                    backupCount=backup_count,
                    utc=False,
                    delay=delay
                    )
    file_handler.setFormatter(_format)
    return file_handler


def setup_basic_logging() -> None:
    # logging.basicConfig(stream=MyLogger(gui_logger))
    log_directory = MainSettings.log_directory
    logging.basicConfig(filename=log_directory / 'core.log',
                        level=logging.WARNING,
                        format=FORMATTER_BASIC,
                        datefmt='%Y.%m.%d %H:%M:%S',
                        filemode='a')


def setup_debug_logger(log_level: logging.DEBUG | logging.ERROR) -> None:
    debug_logger = logging.getLogger('debug_logger')
    debug_logger.setLevel(log_level)
    debug_logger.propagate = False
    debug_logger.addHandler(
            get_file_handler(MainSettings.log_debug_file,
                             mode='w',
                             delay=True,
                             _format=FORMATTER
                             )
            )
    if LOCALHOST:
        debug_logger.addHandler(get_console_handler(_format=FORMATTER_SHORT))


def setup_error_logger() -> None:
    debug_logger = logging.getLogger('error_logger')
    debug_logger.setLevel(logging.ERROR)
    debug_logger.propagate = False
    debug_logger.addHandler(
            get_file_handler(MainSettings.log_error_file,
                             mode='a',
                             delay=True,
                             _format=FORMATTER_ERR
                             )
            )
    if LOCALHOST:
        debug_logger.addHandler(get_console_handler(_format=FORMATTER_SHORT))


def setup_form_logger(filename: Path | str) -> None:
    debug_logger = logging.getLogger('form_logger')
    debug_logger.setLevel(logging.INFO)
    debug_logger.propagate = False
    debug_logger.addHandler(
            get_file_handler(MainSettings.log_directory / filename,
                             mode='a',
                             delay=True,
                             _format=FORMATTER_SHORT)
            )
    if LOCALHOST:
        # debug_logger.addHandler(get_console_handler(_format=FORMATTER_SHORT))
        pass


def get_debug_log_level() -> logging.DEBUG | logging.ERROR:
    if MainSettings.log_debug:
        return logging.DEBUG
    return logging.ERROR


setup_basic_logging()
setup_debug_logger(get_debug_log_level())
setup_error_logger()
