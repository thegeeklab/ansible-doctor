#!/usr/bin/env python3
import glob
import os
import sys

from ansibledoctor.Config import SingleConfig
from ansibledoctor.Contstants import YAML_EXTENSIONS
from ansibledoctor.Utils import SingleLog


class Registry:

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
        base_dir = os.getcwd()

        self.log.debug("Scan for files: " + base_dir)

        for extension in extensions:
            for filename in glob.iglob(base_dir + "/**/*." + extension, recursive=True):
                if self._is_excluded_yaml_file(filename, base_dir):
                    self.log.debug("Excluding: " + filename)
                else:
                    self.log.debug("Adding to role:" + base_dir + " => " + filename)
                    self._doc.append(filename)

    # TODO: not working...
    def _is_excluded_yaml_file(self, file, base_dir):
        """
        Sub method for handling file exclusions based on the full path starts with.

        :param file:
        :param role_base_dir:
        :return:
        """
        excluded = self.config.config.get("exclude_files")

        is_filtered = False
        for excluded_dir in excluded:
            if file.startswith(base_dir + "/" + excluded_dir):
                is_filtered = True

        return is_filtered
