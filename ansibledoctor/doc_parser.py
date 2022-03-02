#!/usr/bin/env python3
"""Parse static files."""

import fnmatch
from collections import defaultdict

import anyconfig
import ruamel.yaml
from nested_lookup import nested_lookup

from ansibledoctor.annotation import Annotation
from ansibledoctor.config import SingleConfig
from ansibledoctor.contstants import YAML_EXTENSIONS
from ansibledoctor.file_registry import Registry
from ansibledoctor.utils import SingleLog
from ansibledoctor.utils import UnsafeTag
from ansibledoctor.utils import flatten


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

    def _yaml_remove_comments(self, d):
        if isinstance(d, dict):
            for k, v in d.items():
                self._yaml_remove_comments(k)
                self._yaml_remove_comments(v)
        elif isinstance(d, list):
            for elem in d:
                self._yaml_remove_comments(elem)
        try:
            attr = "comment" if isinstance(
                d, ruamel.yaml.scalarstring.ScalarString
            ) else ruamel.yaml.comments.Comment.attrib
            delattr(d, attr)
        except AttributeError:
            pass

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

                        raw = ruamel.yaml.YAML(typ="rt").load(yaml_file)
                        self._yaml_remove_comments(raw)

                        data = defaultdict(dict, raw or {})
                        for key, value in data.items():
                            self._data["var"][key] = {"value": {key: value}}
                    except (
                        ruamel.yaml.composer.ComposerError,
                        ruamel.yaml.scanner.ScannerError,
                        ruamel.yaml.constructor.ConstructorError,
                        ruamel.yaml.constructor.DuplicateKeyError,
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
                        raw = ruamel.yaml.YAML(typ="rt").load(yaml_file)
                        self._yaml_remove_comments(raw)

                        data = defaultdict(dict, raw)
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
                        raw = ruamel.yaml.YAML(typ="rt").load(yaml_file)
                        self._yaml_remove_comments(raw)

                        tags = list(set(flatten(nested_lookup("tags", raw))))
                        for tag in tags:
                            self._data["tag"][tag] = {"value": tag}
                    except (
                        ruamel.yaml.composer.ComposerError, ruamel.yaml.scanner.ScannerError
                    ) as e:
                        message = "{} {}".format(e.context, e.problem)
                        self.log.sysexit_with_message(
                            "Unable to read yaml file {}\n{}".format(rfile, message)
                        )

    def _populate_doc_data(self):
        """Generate the documentation data object."""
        tags = defaultdict(dict)
        for annotation in self.config.get_annotations_names(automatic=True):
            self.logger.info("Finding annotations for: @" + annotation)
            self._annotation_objs[annotation] = Annotation(
                name=annotation, files_registry=self._files_registry
            )
            tags[annotation] = self._annotation_objs[annotation].get_details()

        try:
            anyconfig.merge(self._data, tags, ac_merge=anyconfig.MS_DICTS)
        except ValueError as e:
            self.log.sysexit_with_message("Unable to merge annotation values:\n{}".format(e))

    def get_data(self):
        return self._data
