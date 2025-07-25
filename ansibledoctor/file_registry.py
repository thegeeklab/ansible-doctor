#!/usr/bin/env python3
"""File registry to encapsulate file system related operations."""

import glob
import os

import pathspec
import structlog

from ansibledoctor.config import SingleConfig
from ansibledoctor.constants import YAML_EXTENSIONS


class Registry:
    """Register all yaml files."""

    _doc = {}
    log = None
    config = None

    def __init__(self):
        self._doc = []
        self.config = SingleConfig()
        self.log = structlog.get_logger()
        self._scan_for_yaml_files()

    def get_files(self):
        return self._doc

    def _scan_for_yaml_files(self):
        """
        Search for the yaml files in each project/role root and append to the corresponding object.

        :param base: directory in witch we are searching
        :return: None
        """
        extensions = YAML_EXTENSIONS
        base_dir = self.config.config.base_dir
        excludes = self.config.config.get("exclude_files")
        exclude_spec = pathspec.PathSpec.from_lines("gitwildmatch", excludes)

        self.log.debug("Lookup role files", path=base_dir)

        for extension in extensions:
            pattern = os.path.join(base_dir, "**/*." + extension)
            for filename in glob.iglob(pattern, recursive=True):
                if not exclude_spec.match_file(filename):
                    self.log.debug("Found role file", path=os.path.relpath(filename, base_dir))
                    self._doc.append(filename)
                else:
                    self.log.debug("Skipped role file", path=os.path.relpath(filename, base_dir))
