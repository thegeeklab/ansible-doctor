#!/usr/bin/env python3
"""Doctor exception module."""


class DoctorError(Exception):
    """Define generic exception."""

    def __init__(self, msg, original_exception=""):
        super().__init__(f"{msg}\n{original_exception}")
        self.original_exception = original_exception


class YAMLError(DoctorError):
    """Errors while reading a yaml file."""

    pass


class ConfigError(DoctorError):
    """Errors related to config file handling."""

    pass


class TemplateError(DoctorError):
    """Errors related to template file handling."""
