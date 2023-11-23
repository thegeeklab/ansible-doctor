#!/usr/bin/env python3
"""Global utility methods and classes."""

import logging
import os
import sys
from collections.abc import Iterable

import colorama
from pythonjsonlogger import jsonlogger

import ansibledoctor.exception

CONSOLE_FORMAT = "{}{}[%(levelname)s]{} %(message)s"
JSON_FORMAT = "%(asctime)s %(levelname)s %(message)s"


def strtobool(value):
    """Convert a string representation of truth to true or false."""

    _map = {
        "y": True,
        "yes": True,
        "t": True,
        "true": True,
        "on": True,
        "1": True,
        "n": False,
        "no": False,
        "f": False,
        "false": False,
        "off": False,
        "0": False,
    }

    try:
        return _map[str(value).lower()]
    except KeyError as err:
        raise ValueError(f'"{value}" is not a valid bool value') from err


def to_bool(string):
    return bool(strtobool(str(string)))


def flatten(items):
    for x in items:
        if isinstance(x, Iterable) and not isinstance(x, (str, bytes)):
            yield from flatten(x)
        else:
            yield x


def _should_do_markup():
    py_colors = os.environ.get("PY_COLORS", None)
    if py_colors is not None:
        return to_bool(py_colors)

    return sys.stdout.isatty() and os.environ.get("TERM") != "dumb"


def _split_string(string, delimiter, escape, maxsplit=None):
    result = []
    current_element = []
    iterator = iter(string)
    count_split = 0
    skip_split = False

    for character in iterator:
        if maxsplit and count_split >= maxsplit:
            skip_split = True

        if character == escape and not skip_split:
            try:
                next_character = next(iterator)
                if next_character != delimiter and next_character != escape:
                    # Do not copy the escape character if it is intended to escape either the
                    # delimiter or the escape character itself. Copy the escape character
                    # if it is not used to escape either of these characters.
                    current_element.append(escape)
                current_element.append(next_character)
                count_split += 1
            except StopIteration:
                current_element.append(escape)
        elif character == delimiter and not skip_split:
            result.append("".join(current_element))
            current_element = []
            count_split += 1
        else:
            current_element.append(character)

    result.append("".join(current_element))
    return result


colorama.init(autoreset=True, strip=not _should_do_markup())


class Singleton(type):
    """Meta singleton class."""

    _instances = {}

    def __call__(cls, *args, **kwargs):
        if cls not in cls._instances:
            cls._instances[cls] = super().__call__(*args, **kwargs)
        return cls._instances[cls]


class LogFilter:
    """Exclude log messages above the logged level."""

    def __init__(self, level):
        """
        Initialize a new custom log filter.

        :param level: Log level limit
        :returns: None

        """
        self.__level = level

    def filter(self, logRecord):  # noqa
        # https://docs.python.org/3/library/logging.html#logrecord-attributes
        return logRecord.levelno <= self.__level


class MultilineFormatter(logging.Formatter):
    """Reset color after newline characters."""

    def format(self, record):  # noqa
        record.msg = record.msg.strip().replace("\n", f"\n{colorama.Style.RESET_ALL}... ")
        return logging.Formatter.format(self, record)


class MultilineJsonFormatter(jsonlogger.JsonFormatter):
    """Remove newline characters."""

    def format(self, record):  # noqa
        record.msg = record.msg.replace("\n", " ")
        return jsonlogger.JsonFormatter.format(self, record)


class Log:
    """Handle logging."""

    def __init__(self, level=logging.WARNING, name="ansibledoctor", json=False):
        self.logger = logging.getLogger(name)
        self.logger.setLevel(level)
        self.logger.addHandler(self._get_error_handler(json=json))
        self.logger.addHandler(self._get_warning_handler(json=json))
        self.logger.addHandler(self._get_info_handler(json=json))
        self.logger.addHandler(self._get_critical_handler(json=json))
        self.logger.addHandler(self._get_debug_handler(json=json))
        self.logger.propagate = False

    def _get_error_handler(self, json=False):
        handler = logging.StreamHandler(sys.stderr)
        handler.setLevel(logging.ERROR)
        handler.addFilter(LogFilter(logging.ERROR))
        handler.setFormatter(
            MultilineFormatter(
                self.error(
                    CONSOLE_FORMAT.format(
                        colorama.Fore.RED, colorama.Style.BRIGHT, colorama.Style.RESET_ALL
                    )
                )
            )
        )

        if json:
            handler.setFormatter(MultilineJsonFormatter(JSON_FORMAT))

        return handler

    def _get_warning_handler(self, json=False):
        handler = logging.StreamHandler(sys.stdout)
        handler.setLevel(logging.WARNING)
        handler.addFilter(LogFilter(logging.WARNING))
        handler.setFormatter(
            MultilineFormatter(
                self.warning(
                    CONSOLE_FORMAT.format(
                        colorama.Fore.YELLOW, colorama.Style.BRIGHT, colorama.Style.RESET_ALL
                    )
                )
            )
        )

        if json:
            handler.setFormatter(MultilineJsonFormatter(JSON_FORMAT))

        return handler

    def _get_info_handler(self, json=False):
        handler = logging.StreamHandler(sys.stdout)
        handler.setLevel(logging.INFO)
        handler.addFilter(LogFilter(logging.INFO))
        handler.setFormatter(
            MultilineFormatter(
                self.info(
                    CONSOLE_FORMAT.format(
                        colorama.Fore.CYAN, colorama.Style.BRIGHT, colorama.Style.RESET_ALL
                    )
                )
            )
        )

        if json:
            handler.setFormatter(MultilineJsonFormatter(JSON_FORMAT))

        return handler

    def _get_critical_handler(self, json=False):
        handler = logging.StreamHandler(sys.stderr)
        handler.setLevel(logging.CRITICAL)
        handler.addFilter(LogFilter(logging.CRITICAL))
        handler.setFormatter(
            MultilineFormatter(
                self.critical(
                    CONSOLE_FORMAT.format(
                        colorama.Fore.RED, colorama.Style.BRIGHT, colorama.Style.RESET_ALL
                    )
                )
            )
        )

        if json:
            handler.setFormatter(MultilineJsonFormatter(JSON_FORMAT))

        return handler

    def _get_debug_handler(self, json=False):
        handler = logging.StreamHandler(sys.stderr)
        handler.setLevel(logging.DEBUG)
        handler.addFilter(LogFilter(logging.DEBUG))
        handler.setFormatter(
            MultilineFormatter(
                self.debug(
                    CONSOLE_FORMAT.format(
                        colorama.Fore.BLUE, colorama.Style.BRIGHT, colorama.Style.RESET_ALL
                    )
                )
            )
        )

        if json:
            handler.setFormatter(MultilineJsonFormatter(JSON_FORMAT))

        return handler

    def set_level(self, s):
        self.logger.setLevel(s)

    def debug(self, msg):
        """Format info messages and return string."""
        return msg

    def critical(self, msg):
        """Format critical messages and return string."""
        return msg

    def error(self, msg):
        """Format error messages and return string."""
        return msg

    def warning(self, msg):
        """Format warning messages and return string."""
        return msg

    def info(self, msg):
        """Format info messages and return string."""
        return msg

    def _color_text(self, color, msg):
        """
        Colorize strings.

        :param color: colorama color settings
        :param msg: string to colorize
        :returns: string

        """
        return f"{color}{msg}{colorama.Style.RESET_ALL}"

    def sysexit(self, code=1):
        sys.exit(code)

    def sysexit_with_message(self, msg, code=1):
        self.logger.critical(str(msg.strip()))
        self.sysexit(code)


class SingleLog(Log, metaclass=Singleton):
    """Singleton logging class."""

    pass


class FileUtils:
    """Mics static methods for file handling."""

    @staticmethod
    def create_path(path):
        os.makedirs(path, exist_ok=True)

    @staticmethod
    def query_yes_no(question, default=True):
        """
        Ask a yes/no question via input() and return their answer.

        "question" is a string that is presented to the user.
        "default" is the presumed answer if the user just hits <Enter>.
            It must be "yes" (the default), "no" or None (meaning
            an answer is required of the user).

        The "answer" return value is one of "yes" or "no".
        """
        prompt = "[Y/n]" if default else "[N/y]"

        try:
            # input method is safe in python3
            choice = input(f"{question} {prompt} ") or default  # nosec
            return to_bool(choice)
        except (KeyboardInterrupt, ValueError) as e:
            raise ansibledoctor.exception.InputError("Error while reading input", e) from e
