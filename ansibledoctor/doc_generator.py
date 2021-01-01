#!/usr/bin/env python3
"""Prepare output and write compiled jinja2 templates."""

import glob
import ntpath
import os
from functools import reduce

import jinja2.exceptions
import ruamel.yaml
from jinja2 import Environment
from jinja2 import FileSystemLoader
from jinja2.filters import evalcontextfilter

import ansibledoctor.exception
from ansibledoctor.config import SingleConfig
from ansibledoctor.utils import FileUtils
from ansibledoctor.utils import SingleLog


class Generator:
    """Generate documentation from jinja2 templates."""

    def __init__(self, doc_parser):
        self.template_files = []
        self.extension = "j2"
        self._parser = None
        self.config = SingleConfig()
        self.log = SingleLog()
        self.logger = self.log.logger
        self._parser = doc_parser
        self._scan_template()

    def _scan_template(self):
        """
        Search for Jinja2 (.j2) files to apply to the destination.

        :return: None
        """
        template_dir = self.config.get_template()
        if os.path.isdir(template_dir):
            self.logger.info("Using template dir: {}".format(template_dir))
        else:
            self.log.sysexit_with_message("Can not open template dir {}".format(template_dir))

        for file in glob.iglob(template_dir + "/**/*." + self.extension, recursive=True):
            relative_file = file[len(template_dir) + 1:]
            if ntpath.basename(file)[:1] != "_":
                self.logger.debug("Found template file: " + relative_file)
                self.template_files.append(relative_file)
            else:
                self.logger.debug("Ignoring template file: " + relative_file)

    def _create_dir(self, directory):
        if not self.config.config["dry_run"] and not os.path.isdir(directory):
            try:
                os.makedirs(directory, exist_ok=True)
                self.logger.info("Creating dir: " + directory)
            except FileExistsError as e:
                self.log.sysexit_with_message(str(e))

    def _write_doc(self):
        files_to_overwite = []

        for file in self.template_files:
            doc_file = os.path.join(
                self.config.config.get("output_dir"),
                os.path.splitext(file)[0]
            )
            if os.path.isfile(doc_file):
                files_to_overwite.append(doc_file)

        header_file = self.config.config.get("custom_header")
        role_data = self._parser.get_data()
        header_content = ""
        if bool(header_file):
            role_data["internal"]["append"] = True
            try:
                with open(header_file, "r") as a:
                    header_content = a.read()
            except FileNotFoundError as e:
                self.log.sysexit_with_message("Can not open custom header file\n{}".format(str(e)))

        if len(files_to_overwite) > 0 and self.config.config.get("force_overwrite") is False:
            if not self.config.config["dry_run"]:
                self.logger.warn("This files will be overwritten:")
                print(*files_to_overwite, sep="\n")

                try:
                    if not FileUtils.query_yes_no("Do you want to continue?"):
                        self.log.sysexit_with_message("Aborted...")
                except ansibledoctor.exception.InputError as e:
                    self.logger.debug(str(e))
                    self.log.sysexit_with_message("Aborted...")

        for file in self.template_files:
            doc_file = os.path.join(
                self.config.config.get("output_dir"),
                os.path.splitext(file)[0]
            )
            source_file = self.config.get_template() + "/" + file

            self.logger.debug("Writing doc output to: " + doc_file + " from: " + source_file)

            # make sure the directory exists
            self._create_dir(os.path.dirname(doc_file))

            if os.path.exists(source_file) and os.path.isfile(source_file):
                with open(source_file, "r") as template:
                    data = template.read()
                    if data is not None:
                        try:
                            jenv = Environment(  # nosec
                                loader=FileSystemLoader(self.config.get_template()),
                                lstrip_blocks=True,
                                trim_blocks=True
                            )
                            jenv.filters["to_nice_yaml"] = self._to_nice_yaml
                            jenv.filters["deep_get"] = self._deep_get
                            jenv.filters["save_join"] = self._save_join
                            data = jenv.from_string(data).render(role_data, role=role_data)
                            if not self.config.config["dry_run"]:
                                with open(doc_file, "wb") as outfile:
                                    outfile.write(header_content.encode("utf-8"))
                                    outfile.write(data.encode("utf-8"))
                                    self.logger.info("Writing to: " + doc_file)
                            else:
                                self.logger.info("Writing to: " + doc_file)
                        except (
                            jinja2.exceptions.UndefinedError, jinja2.exceptions.TemplateSyntaxError
                        ) as e:
                            self.log.sysexit_with_message(
                                "Jinja2 templating error while loading file: '{}'\n{}".format(
                                    file, str(e)
                                )
                            )
                        except UnicodeEncodeError as e:
                            self.log.sysexit_with_message(
                                "Unable to print special characters\n{}".format(str(e))
                            )

    def _to_nice_yaml(self, a, indent=4, *args, **kw):
        """Make verbose, human readable yaml."""
        yaml = ruamel.yaml.YAML()
        yaml.indent(mapping=indent, sequence=(indent * 2), offset=indent)
        stream = ruamel.yaml.compat.StringIO()
        yaml.dump(a, stream, **kw)
        return stream.getvalue().rstrip()

    def _deep_get(self, _, dictionary, keys, *args, **kw):
        default = None
        return reduce(
            lambda d, key: d.get(key, default)
            if isinstance(d, dict) else default, keys.split("."), dictionary
        )

    @evalcontextfilter
    def _save_join(self, eval_ctx, value, d=u"", attribute=None):
        if isinstance(value, str):
            value = [value]
        return jinja2.filters.do_join(eval_ctx, value, d, attribute=None)

    def render(self):
        self.logger.info("Using output dir: " + self.config.config.get("output_dir"))
        self._write_doc()
