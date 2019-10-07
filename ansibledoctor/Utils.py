#!/usr/bin/python3
import os
import pprint
import sys

import yaml


class Singleton(type):
    _instances = {}

    def __call__(cls, *args, **kwargs):
        if cls not in cls._instances:
            cls._instances[cls] = super(Singleton, cls).__call__(*args, **kwargs)
        return cls._instances[cls]


class Log:
    levels = {
        "trace": -1,
        "debug": 0,
        "info": 1,
        "warn": 2,
        "error": 3,
    }
    log_level = 1

    def __init__(self, level=1):
        self.set_level(level)

    def set_level(self, s):

        if isinstance(s, str):
            for level, v in self.levels.items():
                if level == s:
                    self.log_level = v
        elif isinstance(s, int):
            if s in range(4):
                self.log_level = s

    def trace(self, msg, h=""):
        if self.log_level <= -1:
            self._p("*TRACE*: " + h, msg)

    def debug(self, msg, h=""):
        if self.log_level <= 0:
            self._p("*DEBUG*: " + h, msg)

    def info(self, msg, h=""):
        if self.log_level <= 1:
            self._p("*INFO*: " + h, msg)

    def warn(self, msg, h=""):
        if self.log_level <= 2:
            self._p("*WARN*: " + h, msg)

    def error(self, msg, h=""):
        if self.log_level <= 3:
            self._p("*ERROR*: " + h, msg)

    @staticmethod
    def _p(head, msg, print_type=True):

        if isinstance(msg, list):
            t = " <list>" if print_type else ""
            print(head + t)
            i = 0
            for line in msg:
                print("  [" + str(i) + "]: " + str(line))
                i += 1

        elif isinstance(msg, dict):
            t = " <dict>" if print_type else ""
            print(head + t)
            pprint.pprint(msg)
        else:
            print(head + str(msg))

    @staticmethod
    def print(msg, data):
        Log._p(msg, data, False)


class SingleLog(Log, metaclass=Singleton):
    pass


class FileUtils:
    @staticmethod
    def create_path(path):
        os.makedirs(path, exist_ok=True)

    # http://code.activestate.com/recipes/577058/
    @staticmethod
    def query_yes_no(question, default="yes"):
        """Ask a yes/no question via input() and return their answer.

        "question" is a string that is presented to the user.
        "default" is the presumed answer if the user just hits <Enter>.
            It must be "yes" (the default), "no" or None (meaning
            an answer is required of the user).

        The "answer" return value is one of "yes" or "no".
        """
        valid = {"yes": "yes", "y": "yes", "ye": "yes",
                 "no": "no", "n": "no"}
        if default is None:
            prompt = " [y/n] "
        elif default == "yes":
            prompt = " [Y/n] "
        elif default == "no":
            prompt = " [y/N] "
        else:
            raise ValueError("Invalid default answer: '%s'" % default)

        while 1:
            choice = input(question + prompt).lower()
            if default is not None and choice == "":
                return default
            elif choice in valid.keys():
                return valid[choice]
            else:
                sys.stdout.write("Please respond with 'yes' or 'no' (or 'y' or 'n').\n")
