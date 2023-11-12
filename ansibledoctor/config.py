#!/usr/bin/env python3
"""Global settings definition."""

import os

import anyconfig
import environs
import jsonschema.exceptions
import ruamel.yaml
from appdirs import AppDirs
from jsonschema._utils import format_as_index

import ansibledoctor.exception
from ansibledoctor.utils import Singleton

config_dir = AppDirs("ansible-doctor").user_config_dir
default_config_file = os.path.join(config_dir, "config.yml")
default_envs_prefix = "ANSIBLE_DOCTOR_"


class Config:
    """
    Create an object with all necessary settings.

    Settings are loade from multiple locations in defined order (last wins):
    - default settings defined by `self._get_defaults()`
    - yaml config file, defaults to OS specific user config dir (https://pypi.org/project/appdirs/)
    - provides cli parameters
    """

    SETTINGS = {
        "config_file": {
            "default": default_config_file,
            "env": "CONFIG_FILE",
            "type": environs.Env().str,
        },
        "base_dir": {
            "default": os.getcwd(),
            "refresh": os.getcwd,
            "env": "BASE_DIR",
            "type": environs.Env().str,
        },
        "role_name": {
            "default": "",
            "env": "ROLE_NAME",
            "type": environs.Env().str,
        },
        "dry_run": {
            "default": False,
            "env": "DRY_RUN",
            "file": True,
            "type": environs.Env().bool,
        },
        "logging.level": {
            "default": "WARNING",
            "env": "LOG_LEVEL",
            "file": True,
            "type": environs.Env().str,
        },
        "logging.json": {
            "default": False,
            "env": "LOG_JSON",
            "file": True,
            "type": environs.Env().bool,
        },
        "output_dir": {
            "default": os.getcwd(),
            "refresh": os.getcwd,
            "env": "OUTPUT_DIR",
            "file": True,
            "type": environs.Env().str,
        },
        "recursive": {
            "default": False,
            "env": "RECURSIVE",
            "type": environs.Env().bool,
        },
        "template_dir": {
            "default": os.path.join(os.path.dirname(os.path.realpath(__file__)), "templates"),
            "env": "TEMPLATE_DIR",
            "file": True,
            "type": environs.Env().str,
        },
        "template": {
            "default": "readme",
            "env": "TEMPLATE",
            "file": True,
            "type": environs.Env().str,
        },
        "template_autotrim": {
            "default": True,
            "env": "TEMPLATE_AUTOTRIM",
            "file": True,
            "type": environs.Env().bool,
        },
        "force_overwrite": {
            "default": False,
            "env": "FORCE_OVERWRITE",
            "file": True,
            "type": environs.Env().bool,
        },
        "custom_header": {
            "default": "",
            "env": "CUSTOM_HEADER",
            "file": True,
            "type": environs.Env().str,
        },
        "exclude_files": {
            "default": [],
            "env": "EXCLUDE_FILES",
            "file": True,
            "type": environs.Env().list,
        },
        "exclude_tags": {
            "default": [],
            "env": "EXCLUDE_TAGS",
            "file": True,
            "type": environs.Env().list,
        },
        "role_detection": {
            "default": True,
            "env": "ROLE_DETECTION",
            "file": True,
            "type": environs.Env().bool,
        },
    }

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

    def __init__(self, args=None):
        """
        Initialize a new settings class.

        :param args: An optional dict of options, arguments and commands from the CLI.
        :param config_file: An optional path to a yaml config file.
        :returns: None

        """
        if args is None:
            self._args = {}
        else:
            self._args = args
        self._schema = None
        self.config = None
        self.is_role = False
        self.set_config()

    def _get_args(self, args):
        cleaned = dict(filter(lambda item: item[1] is not None, args.items()))

        normalized = {}
        for key, value in cleaned.items():
            normalized = self._add_dict_branch(normalized, key.split("."), value)

        # Override correct log level from argparse
        levels = ["DEBUG", "INFO", "WARNING", "ERROR", "CRITICAL"]
        log_level = levels.index(self.SETTINGS["logging.level"]["default"])
        if normalized.get("logging"):
            for adjustment in normalized["logging"]["level"]:
                log_level = min(len(levels) - 1, max(log_level + adjustment, 0))
            normalized["logging"]["level"] = levels[log_level]

        return normalized

    def _get_defaults(self):
        normalized = {}
        for key, item in self.SETTINGS.items():
            if item.get("refresh"):
                item["default"] = item["refresh"]()
            normalized = self._add_dict_branch(normalized, key.split("."), item["default"])

        self.schema = anyconfig.gen_schema(normalized)
        return normalized

    def _get_envs(self):
        normalized = {}
        for key, item in self.SETTINGS.items():
            if item.get("env"):
                envname = f"{default_envs_prefix}{item['env']}"
                try:
                    value = item["type"](envname)
                    normalized = self._add_dict_branch(normalized, key.split("."), value)
                except environs.EnvError as e:
                    if f'"{envname}" not set' in str(e):
                        pass
                    else:
                        raise ansibledoctor.exception.ConfigError(
                            "Unable to read environment variable", str(e)
                        ) from e

        return normalized

    def set_config(self, base_dir=None):
        args = self._get_args(self._args)
        envs = self._get_envs()
        defaults = self._get_defaults()

        self.recursive = defaults.get("recursive")
        if envs.get("recursive"):
            self.recursive = envs.get("recursive")
        if args.get("recursive"):
            self.recursive = args.get("recursive")
        if "recursive" in defaults:
            defaults.pop("recursive")

        self.config_file = defaults.get("config_file")
        if envs.get("config_file"):
            self.config_file = self._normalize_path(envs.get("config_file"))
        if args.get("config_file"):
            self.config_file = self._normalize_path(args.get("config_file"))
        if "config_file" in defaults:
            defaults.pop("config_file")

        self.base_dir = defaults.get("base_dir")
        if envs.get("base_dir"):
            self.base_dir = self._normalize_path(envs.get("base_dir"))
        if args.get("base_dir"):
            self.base_dir = self._normalize_path(args.get("base_dir"))
        if base_dir:
            self.base_dir = base_dir
        if "base_dir" in defaults:
            defaults.pop("base_dir")

        self.is_role = os.path.isdir(os.path.join(self.base_dir, "tasks"))

        # compute role_name default
        defaults["role_name"] = os.path.basename(self.base_dir)

        source_files = []
        source_files.append((self.config_file, False))
        source_files.append((os.path.join(os.getcwd(), ".ansibledoctor"), True))
        source_files.append((os.path.join(os.getcwd(), ".ansibledoctor.yml"), True))
        source_files.append((os.path.join(os.getcwd(), ".ansibledoctor.yaml"), True))

        for config, first_found in source_files:
            if config and os.path.exists(config):
                with open(config, encoding="utf8") as stream:
                    s = stream.read()
                    try:
                        file_dict = ruamel.yaml.YAML(typ="safe", pure=True).load(s)
                    except (
                        ruamel.yaml.composer.ComposerError,
                        ruamel.yaml.scanner.ScannerError,
                    ) as e:
                        message = f"{e.context} {e.problem}"
                        raise ansibledoctor.exception.ConfigError(
                            f"Unable to read config file: {config}", message
                        ) from e

                    if self._validate(file_dict):
                        anyconfig.merge(defaults, file_dict, ac_merge=anyconfig.MS_DICTS)
                        defaults["logging"]["level"] = defaults["logging"]["level"].upper()

                    self.config_file = config
                    if first_found:
                        break

        if self._validate(envs):
            anyconfig.merge(defaults, envs, ac_merge=anyconfig.MS_DICTS)

        if self._validate(args):
            anyconfig.merge(defaults, args, ac_merge=anyconfig.MS_DICTS)

        fix_files = ["output_dir", "template_dir", "custom_header"]
        for filename in fix_files:
            if defaults[filename] and defaults[filename] != "":
                defaults[filename] = self._normalize_path(defaults[filename])

        defaults["logging"]["level"] = defaults["logging"]["level"].upper()

        self.config = defaults

    def _normalize_path(self, path):
        if not os.path.isabs(path):
            base = os.path.join(os.getcwd(), path)
            return os.path.abspath(os.path.expanduser(os.path.expandvars(base)))

        return path

    def _validate(self, config):
        try:
            anyconfig.validate(config, self.schema, ac_schema_safe=False)
        except jsonschema.exceptions.ValidationError as e:
            schema_error = "Failed validating '{validator}' in schema{schema}\n{message}".format(
                validator=e.validator,
                schema=format_as_index(list(e.relative_schema_path)[:-1]),
                message=e.message,
            )
            raise ansibledoctor.exception.ConfigError("Configuration error", schema_error) from e

        return True

    def _add_dict_branch(self, tree, vector, value):
        key = vector[0]
        tree[key] = (
            value
            if len(vector) == 1
            else self._add_dict_branch(tree[key] if key in tree else {}, vector[1:], value)
        )
        return tree

    def get_annotations_definition(self, automatic=True):
        annotations = {}
        if automatic:
            for k, item in self.ANNOTATIONS.items():
                if "automatic" in item and item["automatic"]:
                    annotations[k] = item
        return annotations

    def get_annotations_names(self, automatic=True):
        annotations = []
        if automatic:
            for k, item in self.ANNOTATIONS.items():
                if "automatic" in item and item["automatic"]:
                    annotations.append(k)
        return annotations

    def get_template(self):
        """
        Get the base dir for the template to use.

        :return: str abs path
        """
        template_dir = self.config.get("template_dir")
        template = self.config.get("template")
        return os.path.realpath(os.path.join(template_dir, template))


class SingleConfig(Config, metaclass=Singleton):
    """Singleton config class."""

    pass
