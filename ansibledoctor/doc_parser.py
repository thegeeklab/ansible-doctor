#!/usr/bin/env python3
"""Parse static files."""

import fnmatch
from collections import defaultdict

import anyconfig
import structlog

from ansibledoctor.annotation import Annotation
from ansibledoctor.config import SingleConfig
from ansibledoctor.constants import YAML_EXTENSIONS
from ansibledoctor.exception import YAMLError
from ansibledoctor.file_registry import Registry
from ansibledoctor.utils import flatten, sys_exit_with_message
from ansibledoctor.utils.yaml_helper import parse_yaml, parse_yaml_ansible


class Parser:
    """Parse yaml files."""

    def __init__(self):
        self._annotation_objs = {}
        self._data = defaultdict(dict)
        self.config = SingleConfig()
        self.log = structlog.get_logger()
        self._files_registry = Registry()
        self._parse_meta_file()
        self._parse_var_files()
        self._parse_argument_specs()
        self._parse_task_tags()
        self._populate_doc_data()

    def _parse_var_files(self):
        for rfile in self._files_registry.get_files():
            # Only parse YAML files in defaults/main and vars/main directories
            is_defaults_main = any(
                fnmatch.fnmatch(rfile, "*/defaults/main." + ext) for ext in YAML_EXTENSIONS
            )
            is_vars_main = any(
                fnmatch.fnmatch(rfile, "*/vars/main." + ext) for ext in YAML_EXTENSIONS
            )

            if is_defaults_main or is_vars_main:
                with open(rfile, encoding="utf8") as yaml_file:
                    try:
                        raw = parse_yaml(yaml_file)
                    except YAMLError as e:
                        sys_exit_with_message("Failed to read yaml file", path=rfile, error=e)

                    data = defaultdict(dict, raw or {})

                    for key, value in data.items():
                        self._data["var"][key] = {"value": {key: value}}

    def _parse_meta_file(self):
        self._data["meta"]["name"] = {"value": self.config.config["role_name"]}

        for rfile in self._files_registry.get_files():
            if any("meta/main." + ext in rfile for ext in YAML_EXTENSIONS):
                with open(rfile, encoding="utf8") as yaml_file:
                    try:
                        raw = parse_yaml(yaml_file)
                    except YAMLError as e:
                        sys_exit_with_message("Failed to read yaml file", path=rfile, error=e)

                    data = defaultdict(dict, raw)
                    if data.get("galaxy_info"):
                        for key, value in data.get("galaxy_info").items():
                            self._data["meta"][key] = {"value": value}

                    if data.get("dependencies") is not None:
                        self._data["meta"]["dependencies"] = {"value": data.get("dependencies")}

    def _parse_argument_specs(self):
        """Parse meta/argument_specs.yml to discover role arguments."""
        for rfile in self._files_registry.get_files():
            if any("meta/argument_specs." + ext in rfile for ext in YAML_EXTENSIONS):
                with open(rfile, encoding="utf8") as yaml_file:
                    try:
                        raw = parse_yaml(yaml_file)
                    except YAMLError as e:
                        sys_exit_with_message("Failed to read yaml file", path=rfile, error=e)

                    if raw.get("argument_specs") and (
                        first_entry := next(iter(raw["argument_specs"]), None)
                    ):
                        description_attributes = {
                            "short_description": "short_description",
                            "description": "description",
                        }

                        first_entry_specs = raw["argument_specs"][first_entry]
                        for attr_key, attr_name in description_attributes.items():
                            if attr_key in first_entry_specs:
                                self._data["meta"][attr_name] = {
                                    "value": first_entry_specs[attr_key]
                                }

                    # Process argument specs for the first entry point
                    if (
                        raw.get("argument_specs")
                        and (first_entry := next(iter(raw["argument_specs"]), None))
                        and "options" in raw["argument_specs"][first_entry]
                    ):
                        for arg_name, arg_spec in raw["argument_specs"][first_entry][
                            "options"
                        ].items():
                            role_attributes = {
                                "description": "description",
                                "type": "type",
                                "required": "required",
                            }

                            # If the variable already exists in defaults, update its metadata
                            if arg_name not in self._data["var"]:
                                # Add new variable from argument specs
                                default_value = (
                                    "_unset_"
                                    if arg_spec.get("required", False)
                                    else arg_spec.get("default", "_unset_")
                                )
                                self._data["var"][arg_name] = {"value": {arg_name: default_value}}

                            for attr_key, attr_name in role_attributes.items():
                                if attr_key in arg_spec:
                                    self._data["var"][arg_name][attr_name] = arg_spec[attr_key]

    def _parse_task_tags(self):
        for rfile in self._files_registry.get_files():
            if any(fnmatch.fnmatch(rfile, "*/tasks/*." + ext) for ext in YAML_EXTENSIONS):
                with open(rfile, encoding="utf8") as yaml_file:
                    try:
                        raw = parse_yaml_ansible(yaml_file)
                    except YAMLError as e:
                        sys_exit_with_message("Failed to read yaml file", path=rfile, error=e)

                    tags = []
                    for task in raw:
                        task_tags = task.get("tags", [])
                        if isinstance(task_tags, str):
                            task_tags = [task_tags]

                        for tag in task_tags:
                            if tag not in self.config.config["exclude_tags"]:
                                tags.append(tag)

                    for tag in flatten(tags):
                        self._data["tag"][tag] = {"value": tag}

    def _populate_doc_data(self):
        """Generate the documentation data object."""
        tags = defaultdict(dict)
        for annotation in self.config.get_annotations_names(automatic=True):
            self.log.info(f"Lookup annotation @{annotation}")
            self._annotation_objs[annotation] = Annotation(
                name=annotation, files_registry=self._files_registry
            )
            tags[annotation] = self._annotation_objs[annotation].get_details()

        try:
            anyconfig.merge(self._data, tags, ac_merge=anyconfig.MS_DICTS)
        except ValueError as e:
            sys_exit_with_message("Failed to merge annotation values", error=e)

    def get_data(self):
        return self._data
