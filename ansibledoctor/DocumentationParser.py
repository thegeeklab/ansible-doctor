#!/usr/bin/env python3
"""Parse static files."""

import fnmatch
import json
import os
from collections import defaultdict

import anyconfig
import yaml

from ansibledoctor.Annotation import Annotation
from ansibledoctor.Config import SingleConfig
from ansibledoctor.Contstants import YAML_EXTENSIONS
from ansibledoctor.FileRegistry import Registry
from ansibledoctor.Utils import SingleLog


class Parser:
    def __init__(self):
        self._annotation_objs = {}
        self._data = defaultdict(dict)
        self.config = SingleConfig()
        self.log = SingleLog().logger
        self._files_registry = Registry()
        self._parse_meta_file()
        self._parse_vars_file()
        self._populate_doc_data()

    def _parse_vars_file(self):
        extensions = YAML_EXTENSIONS

        for rfile in self._files_registry.get_files():
            if any(fnmatch.fnmatch(rfile, "*/defaults/*." + ext) for ext in extensions):
                with open(rfile, "r", encoding="utf8") as yaml_file:
                    try:
                        data = defaultdict(dict, yaml.load(yaml_file, Loader=yaml.SafeLoader))
                        for key, value in data.items():
                            self._data["var"][key] = {"value": {key: value}}
                    except yaml.YAMLError as exc:
                        print(exc)

    def _parse_meta_file(self):
        extensions = YAML_EXTENSIONS

        for rfile in self._files_registry.get_files():
            if any("meta/main." + ext in rfile for ext in extensions):
                with open(rfile, "r", encoding="utf8") as yaml_file:
                    try:
                        data = defaultdict(dict, yaml.safe_load(yaml_file))
                        if data.get("galaxy_info"):
                            for key, value in data.get("galaxy_info").items():
                                self._data["meta"][key] = {"value": value}

                        if data.get("dependencies") is not None:
                            self._data["meta"]["dependencies"] = {"value": data.get("dependencies")}
                    except yaml.YAMLError as exc:
                        print(exc)

    def _populate_doc_data(self):
        """Generate the documentation data object."""
        tags = defaultdict(dict)
        for annotaion in self.config.get_annotations_names(automatic=True):
            self.log.info("Finding annotations for: @" + annotaion)
            self._annotation_objs[annotaion] = Annotation(name=annotaion, files_registry=self._files_registry)
            tags[annotaion] = self._annotation_objs[annotaion].get_details()
        anyconfig.merge(self._data, tags, ac_merge=anyconfig.MS_DICTS)

    def get_data(self):
        return self._data
