#!/usr/bin/env python3
"""Utility functions for file operations."""

import fnmatch

from ansibledoctor.constants import DEFAULTS_FILE_KEY, VARS_FILE_KEY, YAML_EXTENSIONS


def classify_var_file(rfile: str) -> str | None:
    """Classify a file as a vars or defaults file based on its path."""
    if any(fnmatch.fnmatch(rfile, "*/vars/main." + ext) for ext in YAML_EXTENSIONS):
        return VARS_FILE_KEY
    if any(fnmatch.fnmatch(rfile, "*/defaults/main." + ext) for ext in YAML_EXTENSIONS):
        return DEFAULTS_FILE_KEY
    return None
