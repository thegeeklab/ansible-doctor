#!/usr/bin/env python3
"""Parse static files."""

import fnmatch
from collections import defaultdict

import anyconfig
import ruamel.yaml
from nested_lookup import nested_lookup

from ansibledoctor.Annotation import Annotation
from ansibledoctor.Config import SingleConfig
from ansibledoctor.Contstants import YAML_EXTENSIONS
from ansibledoctor.FileRegistry import Registry
from ansibledoctor.Utils import SingleLog
from ansibledoctor.Utils import UnsafeTag


class Parser:
    """Parse yaml files."""

    def __init__(self):
        self._annotation_objs = {}
        self._data = defaultdict(dict)
        self.config = SingleConfig()
        self.log = SingleLog()
        self.logger = SingleLog().logger
        self._files_registry = Registry()
        self._parse_meta_file()
        self._parse_var_files()
        self._populate_doc_data()

    def _parse_var_files(self):
        for rfile in self._files_registry.get_files():
            if any(fnmatch.fnmatch(rfile, "*/defaults/*." + ext) for ext in YAML_EXTENSIONS):
                with open(rfile, "r", encoding="utf8") as yaml_file:
                    try:
                        ruamel.yaml.add_constructor(
                            UnsafeTag.yaml_tag,
                            UnsafeTag.yaml_constructor,
                            constructor=ruamel.yaml.SafeConstructor
                        )
                        data = defaultdict(dict, (ruamel.yaml.safe_load(yaml_file) or {}))
                        for key, value in data.items():
                            self._data["var"][key] = {"value": {key: value}}
                    except (
                        ruamel.yaml.composer.ComposerError, ruamel.yaml.scanner.ScannerError
                    ) as e:
                        message = "{} {}".format(e.context, e.problem)
                        self.log.sysexit_with_message(
                            "Unable to read yaml file {}\n{}".format(rfile, message)
                        )

    def _parse_meta_file(self):
        for rfile in self._files_registry.get_files():
            if any("meta/main." + ext in rfile for ext in YAML_EXTENSIONS):
                with open(rfile, "r", encoding="utf8") as yaml_file:
                    try:
                        data = defaultdict(dict, ruamel.yaml.safe_load(yaml_file))
                        if data.get("galaxy_info"):
                            for key, value in data.get("galaxy_info").items():
                                self._data["meta"][key] = {"value": value}

                        if data.get("dependencies") is not None:
                            self._data["meta"]["dependencies"] = {
                                "value": data.get("dependencies")
                            }

                        self._data["meta"]["name"] = {"value": self.config.config["role_name"]}
                    except (
                        ruamel.yaml.composer.ComposerError, ruamel.yaml.scanner.ScannerError
                    ) as e:
                        message = "{} {}".format(e.context, e.problem)
                        self.log.sysexit_with_message(
                            "Unable to read yaml file {}\n{}".format(rfile, message)
                        )

    def _parse_task_tags(self):
        for rfile in self._files_registry.get_files():
            if any(fnmatch.fnmatch(rfile, "*/tasks/*." + ext) for ext in YAML_EXTENSIONS):
                with open(rfile, "r", encoding="utf8") as yaml_file:
                    try:
                        data = ruamel.yaml.safe_load(yaml_file)
                    except (
                        ruamel.yaml.composer.ComposerError, ruamel.yaml.scanner.ScannerError
                    ) as e:
                        message = "{} {}".format(e.context, e.problem)
                        self.log.sysexit_with_message(
                            "Unable to read yaml file {}\n{}".format(rfile, message)
                        )

                    tags_found = nested_lookup("tags", data)
                    for tag in tags_found:
                        self._data["tags"][tag] = {}

    def _populate_doc_data(self):
        """Generate the documentation data object."""
        tags = defaultdict(dict)
        for annotaion in self.config.get_annotations_names(automatic=True):
            self.logger.info("Finding annotations for: @" + annotaion)
            self._annotation_objs[annotaion] = Annotation(
                name=annotaion, files_registry=self._files_registry
            )
            tags[annotaion] = self._annotation_objs[annotaion].get_details()

        try:
            anyconfig.merge(self._data, tags, ac_merge=anyconfig.MS_DICTS)
        except ValueError as e:
            self.log.sysexit_with_message("Unable to merge annotation values:\n{}".format(e))

    def get_data(self):
        return self._data
