#!/usr/bin/env python3
"""Custom exceptions."""


class DoctorError(Exception):
    """Generic exception class for ansible-doctor."""

    def __init__(self, msg, original_exception=""):
        super(DoctorError, self).__init__("{msg}\n{org}".format(msg=msg, org=original_exception))
        self.original_exception = original_exception


class ConfigError(DoctorError):
    """Errors related to config file handling."""

    pass


class InputError(DoctorError):
    """Errors related to config file handling."""

    pass
