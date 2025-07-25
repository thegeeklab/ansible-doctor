#!/usr/bin/env python3
"""Utility functions for file operations."""

import fnmatch

from ansibledoctor.constants import DEFAULTS_FILE_KEY, VARS_FILE_KEY, YAML_EXTENSIONS


def classify_var_file(rfile):
    if any("vars/main." + ext in rfile for ext in YAML_EXTENSIONS):
        return VARS_FILE_KEY
    if any(fnmatch.fnmatch(rfile, "*/defaults/*." + ext) for ext in YAML_EXTENSIONS):
        return DEFAULTS_FILE_KEY
    return None
