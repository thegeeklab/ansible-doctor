#!/usr/bin/env python3
"""Global utility methods and classes."""

import os
import sys
from collections.abc import Iterable

import structlog


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


def sysexit(code=1):
    sys.exit(code)


def sysexit_with_message(msg, code=1, **kwargs):
    structlog.get_logger().critical(str(msg).strip(), **kwargs)
    sysexit(code)


class Singleton(type):
    """Meta singleton class."""

    _instances = {}

    def __call__(cls, *args, **kwargs):
        if cls not in cls._instances:
            cls._instances[cls] = super().__call__(*args, **kwargs)
        return cls._instances[cls]


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

        while True:
            try:
                # input method is safe in python3
                choice = input(f"{question} {prompt} ") or default  # nosec
                return to_bool(choice)
            except ValueError:
                print("Invalid input. Please enter 'y' or 'n'.")  # noqa: T201
            except KeyboardInterrupt as e:
                raise e
