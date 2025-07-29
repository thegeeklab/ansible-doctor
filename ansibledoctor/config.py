#!/usr/bin/env python3
"""Global settings definition."""

import logging
import os
import re
from io import StringIO

import colorama
import structlog
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
            "subtypes": ["value", "example", "description", "type", "deprecated", "required"],
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
        tmpl_src = os.path.join(os.path.dirname(os.path.realpath(__file__)), "templates")
        tmpl_provider = ["local", "git"]

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
                    default=f"local>{tmpl_src}",
                    is_type_of=str,
                    condition=lambda x: re.match(r"^(local|git)\s*>\s*", x),
                    messages={
                        "condition": f"Template provider must be one of {tmpl_provider}.",
                    },
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
                Validator(
                    "annotations",
                    default={},
                    is_type_of=dict,
                    condition=lambda x: all(
                        key.lower() in map(str.lower, self.ANNOTATIONS.keys()) for key in x
                    ),
                    messages={
                        "condition": f"Invalid annotation name. "
                        f"Valid annotations are: {', '.join(self.ANNOTATIONS.keys())}",
                    },
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

        self._init_logger()

    def validate(self):
        try:
            self.config.validators.validate_all()
        except ValidationError as e:
            raise ansibledoctor.exception.ConfigError("Configuration error", e.message) from e

    def is_role(self):
        self.config.role_name = self.config.get(
            "role.name", os.path.basename(self.config.base_dir)
        )
        return os.path.isdir(os.path.join(self.config.base_dir, "tasks"))

    def get_annotations_definition(self, automatic=True):
        annotations = {}
        if automatic:
            for k, item in self.ANNOTATIONS.items():
                if item.get("automatic"):
                    # Merge default annotations with user-defined ones
                    merged_annotation = item.copy()
                    user_annotation = self.config.get("annotations", {}).get(k, {})
                    if "subtypes" in user_annotation:
                        # Merge default subtypes with user-defined ones (no duplicates)
                        merged_annotation["subtypes"] = list(
                            set(
                                list(merged_annotation["subtypes"])
                                + list(user_annotation["subtypes"])
                            )
                        )
                    annotations[k] = merged_annotation
        return annotations

    def get_annotations_names(self, automatic=True):
        annotations = []
        if automatic:
            for k, item in self.ANNOTATIONS.items():
                if item.get("automatic"):
                    annotations.append(k)
        return annotations

    def get_output_path(self, template_file):
        """Get the output file path for a template file."""
        dest_path = self.config.get("renderer.dest")
        dest_dir, dest_file = self._parse_output_path(dest_path)

        if dest_file:
            return os.path.join(dest_dir, dest_file)
        return os.path.join(dest_dir, os.path.splitext(template_file)[0])

    def _parse_output_path(self, output_path):
        output_path = os.path.expanduser(output_path)

        # If path exists, check if it's a directory
        if os.path.exists(output_path):
            if os.path.isdir(output_path):
                return output_path, None
            return os.path.dirname(output_path), os.path.basename(output_path)

        # If path doesn't exist, use heuristics
        # If it has a file extension or doesn't end with separator, treat as file
        if os.path.splitext(output_path)[1] or not output_path.endswith(os.sep):
            return os.path.dirname(output_path) or ".", os.path.basename(output_path)
        # Ends with separator, treat as directory
        return output_path.rstrip(os.sep), None

    def _init_logger(self):
        styles = structlog.dev.ConsoleRenderer.get_default_level_styles()
        styles["debug"] = colorama.Fore.BLUE

        processors = [
            structlog.contextvars.merge_contextvars,
            structlog.processors.add_log_level,
            structlog.processors.StackInfoRenderer(),
            structlog.dev.set_exc_info,
            structlog.processors.TimeStamper(fmt="%Y-%m-%d %H:%M:%S", utc=False),
        ]

        if self.config.logging.json:
            processors.append(ErrorStringifier())
            processors.append(structlog.processors.JSONRenderer())
        else:
            processors.append(MultilineConsoleRenderer(level_styles=styles))

        try:
            structlog.configure(
                processors=processors,
                wrapper_class=structlog.make_filtering_bound_logger(
                    logging.getLevelName(self.config.get("logging.level")),
                ),
            )
            structlog.contextvars.unbind_contextvars()
        except KeyError as e:
            raise ansibledoctor.exception.ConfigError(f"Can not set log level: {e!s}") from e


class ErrorStringifier:
    """A processor that converts exceptions to a string representation."""

    def __call__(self, _, __, event_dict):
        if "error" not in event_dict:
            return event_dict

        err = event_dict.get("error")

        if isinstance(err, Exception):
            event_dict["error"] = f"{err.__class__.__name__}: {err}"

        return event_dict


class MultilineConsoleRenderer(structlog.dev.ConsoleRenderer):
    """A processor for printing multiline strings."""

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    def __call__(self, _, __, event_dict):
        err = None

        if "error" in event_dict:
            err = event_dict.pop("error")

        event_dict = super().__call__(_, __, event_dict)

        if not err:
            return event_dict

        sio = StringIO()
        sio.write(event_dict)

        if isinstance(err, Exception):
            sio.write(
                f"\n{colorama.Fore.RED}{err.__class__.__name__}:"
                f"{colorama.Style.RESET_ALL} {str(err).strip()}"
            )
        else:
            sio.write(f"\n{err.strip()}")

        return sio.getvalue()


class SingleConfig(Config, metaclass=Singleton):
    """Singleton config class."""

    pass
