#!/usr/bin/env python3
"""Parse static files."""

import fnmatch
from collections import defaultdict

import anyconfig

from ansibledoctor.annotation import Annotation
from ansibledoctor.config import SingleConfig
from ansibledoctor.contstants import YAML_EXTENSIONS
from ansibledoctor.exception import YAMLError
from ansibledoctor.file_registry import Registry
from ansibledoctor.utils import SingleLog, flatten
from ansibledoctor.utils.yamlhelper import parse_yaml, parse_yaml_ansible


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
        self._parse_task_tags()
        self._populate_doc_data()

    def _parse_var_files(self):
        for rfile in self._files_registry.get_files():
            if any(fnmatch.fnmatch(rfile, "*/defaults/*." + ext) for ext in YAML_EXTENSIONS):
                with open(rfile, encoding="utf8") as yamlfile:
                    try:
                        raw = parse_yaml(yamlfile)
                    except YAMLError as e:
                        self.log.sysexit_with_message(f"Unable to read yaml file {rfile}\n{e}")

                    data = defaultdict(dict, raw or {})

                    for key, value in data.items():
                        self._data["var"][key] = {"value": {key: value}}

    def _parse_meta_file(self):
        self._data["meta"]["name"] = {"value": self.config.config["role_name"]}

        for rfile in self._files_registry.get_files():
            if any("meta/main." + ext in rfile for ext in YAML_EXTENSIONS):
                with open(rfile, encoding="utf8") as yamlfile:
                    try:
                        raw = parse_yaml(yamlfile)
                    except YAMLError as e:
                        self.log.sysexit_with_message(f"Unable to read yaml file {rfile}\n{e}")

                    data = defaultdict(dict, raw)
                    if data.get("galaxy_info"):
                        for key, value in data.get("galaxy_info").items():
                            self._data["meta"][key] = {"value": value}

                    if data.get("dependencies") is not None:
                        self._data["meta"]["dependencies"] = {"value": data.get("dependencies")}

    def _parse_task_tags(self):
        for rfile in self._files_registry.get_files():
            if any(fnmatch.fnmatch(rfile, "*/tasks/*." + ext) for ext in YAML_EXTENSIONS):
                with open(rfile, encoding="utf8") as yamlfile:
                    try:
                        raw = parse_yaml_ansible(yamlfile)
                    except YAMLError as e:
                        self.log.sysexit_with_message(f"Unable to read yaml file {rfile}\n{e}")

                    tags = [
                        task.get("tags")
                        for task in raw
                        if task.get("tags")
                        and task.get("tags") not in self.config.config["exclude_tags"]
                    ]

                    for tag in flatten(tags):
                        self._data["tag"][tag] = {"value": tag}

    def _populate_doc_data(self):
        """Generate the documentation data object."""
        tags = defaultdict(dict)
        for annotation in self.config.get_annotations_names(automatic=True):
            self.logger.info(f"Finding annotations for: @{annotation}")
            self._annotation_objs[annotation] = Annotation(
                name=annotation, files_registry=self._files_registry
            )
            tags[annotation] = self._annotation_objs[annotation].get_details()

        try:
            anyconfig.merge(self._data, tags, ac_merge=anyconfig.MS_DICTS)
        except ValueError as e:
            self.log.sysexit_with_message(f"Unable to merge annotation values:\n{e}")

    def get_data(self):
        return self._data
