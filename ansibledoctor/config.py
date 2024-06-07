#!/usr/bin/env python3
"""Global settings definition."""

import os

from appdirs import AppDirs
from dynaconf import Dynaconf, ValidationError, Validator

import ansibledoctor.exception
from ansibledoctor.utils import Singleton


class Config:
    """Create configuration object."""

    ANNOTATIONS = {
        "meta": {
            "name": "meta",
            "automatic": True,
            "subtypes": ["value"],
            "allow_multiple": False,
        },
        "todo": {
            "name": "todo",
            "automatic": True,
            "subtypes": ["value"],
            "allow_multiple": True,
        },
        "var": {
            "name": "var",
            "automatic": True,
            "subtypes": ["value", "example", "description", "type", "deprecated"],
            "allow_multiple": False,
        },
        "example": {
            "name": "example",
            "automatic": True,
            "subtypes": [],
            "allow_multiple": False,
        },
        "tag": {
            "name": "tag",
            "automatic": True,
            "subtypes": ["value", "description"],
            "allow_multiple": False,
        },
    }

    def __init__(self):
        self.config_files = [
            os.path.join(AppDirs("ansible-doctor").user_config_dir, "config.yml"),
            ".ansibledoctor",
            ".ansibledoctor.yml",
            ".ansibledoctor.yaml",
        ]
        self.config_merge = True
        self.args = {}
        self.load()

    def load(self, root_path=None, args=None):
        if args:
            if args.get("config_file"):
                self.config_merge = False
                self.config_files = [os.path.abspath(args.get("config_file"))]
                args.pop("config_file")

            self.args = args

        self.config = Dynaconf(
            envvar_prefix="ANSIBLE_DOCTOR",
            merge_enabled=self.config_merge,
            core_loaders=["YAML"],
            root_path=root_path,
            settings_files=self.config_files,
            fresh_vars=["base_dir", "output_dir"],
            validators=[
                Validator(
                    "base_dir",
                    default=os.getcwd(),
                    apply_default_on_none=True,
                    is_type_of=str,
                ),
                Validator(
                    "dry_run",
                    default=False,
                    is_type_of=bool,
                ),
                Validator(
                    "recursive",
                    default=False,
                    is_type_of=bool,
                ),
                Validator(
                    "exclude_files",
                    default=[],
                    is_type_of=list,
                ),
                Validator(
                    "exclude_tags",
                    default=[],
                    is_type_of=list,
                ),
                Validator(
                    "role.name",
                    is_type_of=str,
                ),
                Validator(
                    "role.autodetect",
                    default=True,
                    is_type_of=bool,
                ),
                Validator(
                    "logging.level",
                    default="WARNING",
                    is_in=[
                        "DEBUG",
                        "INFO",
                        "WARNING",
                        "ERROR",
                        "CRITICAL",
                        "debug",
                        "info",
                        "warning",
                        "error",
                        "critical",
                    ],
                ),
                Validator(
                    "logging.json",
                    default=False,
                    is_type_of=bool,
                ),
                Validator(
                    "recursive",
                    default=False,
                    is_type_of=bool,
                ),
                Validator(
                    "template.src",
                    default=os.path.join(os.path.dirname(os.path.realpath(__file__)), "templates"),
                    is_type_of=str,
                ),
                Validator(
                    "template.name",
                    default="readme",
                    is_type_of=str,
                ),
                Validator(
                    "template.options.tabulate_variables",
                    default=False,
                    is_type_of=bool,
                ),
                Validator(
                    "renderer.autotrim",
                    default=True,
                    is_type_of=bool,
                ),
                Validator(
                    "renderer.include_header",
                    default="",
                    is_type_of=str,
                ),
                Validator(
                    "renderer.dest",
                    default=os.path.relpath(os.getcwd()),
                    is_type_of=str,
                ),
                Validator(
                    "renderer.force_overwrite",
                    default=False,
                    is_type_of=bool,
                ),
            ],
        )

        self.validate()

        # Override correct log level from argparse
        levels = ["DEBUG", "INFO", "WARNING", "ERROR", "CRITICAL"]
        log_level = levels.index(self.config.logging.level.upper())
        if self.args.get("logging.level") and isinstance(self.args["logging.level"], list):
            for lvl in self.args["logging.level"]:
                log_level = min(len(levels) - 1, max(log_level + lvl, 0))

        self.args["logging__level"] = levels[log_level]

        if root_path:
            self.args["base_dir"] = root_path

        self.config.update(self.args)
        self.validate()

    def validate(self):
        try:
            self.config.validators.validate_all()
        except ValidationError as e:
            raise ansibledoctor.exception.ConfigError("Configuration error", e.message) from e

    def is_role(self):
        self.config.role_name = self.config.get(
            "role_name", os.path.basename(self.config.base_dir)
        )
        return os.path.isdir(os.path.join(self.config.base_dir, "tasks"))

    def get_annotations_definition(self, automatic=True):
        annotations = {}
        if automatic:
            for k, item in self.ANNOTATIONS.items():
                if item.get("automatic"):
                    annotations[k] = item
        return annotations

    def get_annotations_names(self, automatic=True):
        annotations = []
        if automatic:
            for k, item in self.ANNOTATIONS.items():
                if item.get("automatic"):
                    annotations.append(k)
        return annotations

    def get_template(self):
        """
        Get the base dir for the template to use.

        :return: str abs path
        """
        template_base = self.config.get("template.src")
        template_name = self.config.get("template.name")
        return os.path.realpath(os.path.join(template_base, template_name))


class SingleConfig(Config, metaclass=Singleton):
    """Singleton config class."""

    pass
