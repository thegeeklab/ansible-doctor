#!/usr/bin/env python3
"""Doctor exception module."""

from typing import Any


class DoctorError(Exception):
    """Define generic exception."""

    def __init__(self, msg: Any, original_exception: Any = ""):
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
