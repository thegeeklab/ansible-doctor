#!/usr/bin/env python3
"""Global settings definition."""

import os
import sys

import anyconfig
import jsonschema.exceptions
import yaml
from appdirs import AppDirs
from jsonschema._utils import format_as_index
from pkg_resources import resource_filename

import ansibledoctor.Exception
from ansibledoctor.Utils import Singleton

config_dir = AppDirs("ansible-doctor").user_config_dir
default_config_file = os.path.join(config_dir, "config.yml")


class Config():
    """
    Create an object with all necessary settings.

    Settings are loade from multiple locations in defined order (last wins):
    - default settings defined by `self._get_defaults()`
    - yaml config file, defaults to OS specific user config dir (https://pypi.org/project/appdirs/)
    - provides cli parameters
    """

    def __init__(self, args={}, config_file=None):
        """
        Initialize a new settings class.

        :param args: An optional dict of options, arguments and commands from the CLI.
        :param config_file: An optional path to a yaml config file.
        :returns: None

        """
        self.config_file = None
        self.schema = None
        self.args = self._set_args(args)
        self.base_dir = self._set_base_dir()
        self.is_role = self._set_is_role() or False
        self.dry_run = self._set_dry_run() or False
        self.config = self._get_config()
        self._annotations = self._set_annotations()
        self._post_processing()

    def _set_args(self, args):
        defaults = self._get_defaults()
        if args.get("config_file"):
            self.config_file = os.path.abspath(os.path.expanduser(os.path.expandvars(args.get("config_file"))))
        else:
            self.config_file = default_config_file

        args.pop("config_file", None)
        tmp_args = dict(filter(lambda item: item[1] is not None, args.items()))

        tmp_dict = {}
        for key, value in tmp_args.items():
            tmp_dict = self._add_dict_branch(tmp_dict, key.split("."), value)

        # Override correct log level from argparse
        levels = ["DEBUG", "INFO", "WARNING", "ERROR", "CRITICAL"]
        log_level = levels.index(defaults["logging"]["level"])
        if tmp_dict.get("logging"):
            for adjustment in tmp_dict["logging"]["level"]:
                log_level = min(len(levels) - 1, max(log_level + adjustment, 0))
            tmp_dict["logging"]["level"] = levels[log_level]

        return tmp_dict

    def _get_defaults(self):
        default_template = os.path.join(os.path.dirname(os.path.realpath(__file__)), "templates")
        defaults = {
            "logging": {
                "level": "WARNING",
                "json": False
            },
            "output_dir": os.getcwd(),
            "template_dir": default_template,
            "template": "readme",
            "force_overwrite": False,
            "appent_to_file": "",
            "exclude_files": [],
        }

        self.schema = anyconfig.gen_schema(defaults)
        return defaults

    def _get_config(self):
        defaults = self._get_defaults()
        source_files = []
        source_files.append(self.config_file)
        source_files.append(os.path.join(self.base_dir, ".ansibledoctor"))
        source_files.append(os.path.join(self.base_dir, ".ansibledoctor.yml"))
        source_files.append(os.path.join(self.base_dir, ".ansibledoctor.yaml"))
        cli_options = self.args

        for config in source_files:
            if config and os.path.exists(config):
                with open(config, "r", encoding="utf8") as stream:
                    s = stream.read()
                    try:
                        sdict = yaml.safe_load(s)
                    except yaml.parser.ParserError as e:
                        message = "{}\n{}".format(e.problem, str(e.problem_mark))
                        raise ansibledoctor.Exception.ConfigError("Unable to read file", message)

                    if self._validate(sdict):
                        anyconfig.merge(defaults, sdict, ac_merge=anyconfig.MS_DICTS)
                        defaults["logging"]["level"] = defaults["logging"]["level"].upper()

        if cli_options and self._validate(cli_options):
            anyconfig.merge(defaults, cli_options, ac_merge=anyconfig.MS_DICTS)

        return defaults

    def _set_annotations(self):
        annotations = {
            "meta": {
                "name": "meta",
                "automatic": True
            },
            "todo": {
                "name": "todo",
                "automatic": True,
            },
            "var": {
                "name": "var",
                "automatic": True,
            },
            "example": {
                "name": "example",
                "regex": r"(\#\ *\@example\ *\: *.*)"
            },
            "tag": {
                "name": "tag",
                "automatic": True,
            },
        }
        return annotations

    def _set_base_dir(self):
        if self.args.get("base_dir"):
            real = os.path.abspath(os.path.expanduser(os.path.expandvars(self.args.get("base_dir"))))
        else:
            real = os.getcwd()
        return real

    def _set_is_role(self):
        if os.path.isdir(os.path.join(self.base_dir, "tasks")):
            return True

    def _set_dry_run(self):
        if self.args.get("dry_run"):
            return True

    def _post_processing(self):
        # Override append file path
        append_file = self.config.get("append_to_file")
        if append_file:
            if not os.path.isabs(os.path.expanduser(os.path.expandvars(append_file))):
                append_file = os.path.join(self.base_dir, append_file)

            self.config["append_to_file"] = os.path.abspath(os.path.expanduser(os.path.expandvars(append_file)))

    def _validate(self, config):
        try:
            anyconfig.validate(config, self.schema, ac_schema_safe=False)
        except jsonschema.exceptions.ValidationError as e:
            schema_error = "Failed validating '{validator}' in schema{schema}\n{message}".format(
                validator=e.validator,
                schema=format_as_index(list(e.relative_schema_path)[:-1]),
                message=e.message
            )
            raise ansibledoctor.Exception.ConfigError("Configuration error", schema_error)

        return True

    def _add_dict_branch(self, tree, vector, value):
        key = vector[0]
        tree[key] = value \
            if len(vector) == 1 \
            else self._add_dict_branch(tree[key] if key in tree else {},
                                       vector[1:], value)
        return tree

    def get_annotations_definition(self, automatic=True):
        annotations = {}
        if automatic:
            for k, item in self._annotations.items():
                if "automatic" in item.keys() and item["automatic"]:
                    annotations[k] = item
        return annotations

    def get_annotations_names(self, automatic=True):
        annotations = []
        if automatic:
            for k, item in self._annotations.items():
                if "automatic" in item.keys() and item["automatic"]:
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
    pass
