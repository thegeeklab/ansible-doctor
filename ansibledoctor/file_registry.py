#!/usr/bin/env python3
"""File registry to encapsulate file system related operations."""

import glob
import os

import pathspec

from ansibledoctor.config import SingleConfig
from ansibledoctor.contstants import YAML_EXTENSIONS
from ansibledoctor.utils import SingleLog


class Registry:
    """Register all yaml files."""

    _doc = {}
    log = None
    config = None

    def __init__(self):
        self._doc = []
        self.config = SingleConfig()
        self.log = SingleLog().logger
        self._scan_for_yamls()

    def get_files(self):
        return self._doc

    def _scan_for_yamls(self):
        """
        Search for the yaml files in each project/role root and append to the corresponding object.

        :param base: directory in witch we are searching
        :return: None
        """
        extensions = YAML_EXTENSIONS
        base_dir = self.config.base_dir
        role_name = os.path.basename(base_dir)
        excludes = self.config.config.get("exclude_files")
        excludespec = pathspec.PathSpec.from_lines("gitwildmatch", excludes)

        self.log.debug(f"Scan for files: {base_dir}")

        for extension in extensions:
            pattern = os.path.join(base_dir, "**/*." + extension)
            for filename in glob.iglob(pattern, recursive=True):
                if not excludespec.match_file(filename):
                    self.log.debug(
                        f"Adding file to '{role_name}': {os.path.relpath(filename, base_dir)}"
                    )
                    self._doc.append(filename)
                else:
                    self.log.debug(f"Excluding file: {os.path.relpath(filename, base_dir)}")
