#!/usr/bin/env python3
"""Prepare output and write compiled jinja2 templates."""

import glob
import ntpath
import os
import re
from functools import reduce

import jinja2.exceptions
import ruamel.yaml
from jinja2 import Environment, FileSystemLoader
from jinja2.filters import pass_eval_context

import ansibledoctor.exception
from ansibledoctor.config import SingleConfig
from ansibledoctor.utils import FileUtils, SingleLog


class Generator:
    """Generate documentation from jinja2 templates."""

    def __init__(self, doc_parser):
        self.config = SingleConfig()
        self.log = SingleLog()
        self.logger = self.log.logger
        self._parser = doc_parser

    def _scan_template(self):
        """
        Search for Jinja2 (.j2) files to apply to the destination.

        :return: None
        """
        template_files = []
        provider, template = self.config.get_template()

        if os.path.isdir(template):
            self.logger.info(f"Using template: {os.path.relpath(template, self.log.ctx)}")
        else:
            self.log.sysexit_with_message(f"Can not open template directory {template}")

        for file in glob.iglob(template + "/**/*.j2", recursive=True):
            relative_file = file[len(template) + 1 :]
            if ntpath.basename(file)[:1] != "_":
                self.logger.debug(f"Found template file: {relative_file}")
                template_files.append(relative_file)
            else:
                self.logger.debug(f"Ignoring template file: {relative_file}")

        return template_files

    def _create_dir(self, directory):
        if not self.config.config["dry_run"] and not os.path.isdir(directory):
            try:
                os.makedirs(directory, exist_ok=True)
                self.logger.info(f"Creating dir: {directory}")
            except FileExistsError as e:
                self.log.sysexit_with_message(e)

    def _write_doc(self):
        files_to_overwite = []
        template_files = self._scan_template()

        for tf in template_files:
            doc_file = os.path.join(
                self.config.config.get("renderer.dest"), os.path.splitext(tf)[0]
            )
            if os.path.isfile(doc_file):
                files_to_overwite.append(doc_file)

        header_file = self.config.config.get("renderer.include_header")
        role_data = self._parser.get_data()
        header_content = ""
        if bool(header_file):
            role_data["internal"]["append"] = True
            try:
                with open(header_file) as a:
                    header_content = a.read()
            except FileNotFoundError as e:
                self.log.sysexit_with_message(f"Can not open custom header file\n{e!s}")

        if (
            len(files_to_overwite) > 0
            and self.config.config.get("renderer.force_overwrite") is False
            and not self.config.config["dry_run"]
        ):
            files_to_overwite_string = "\n".join(files_to_overwite)
            prompt = f"These files will be overwritten:\n{files_to_overwite_string}".replace(
                "\n", "\n... "
            )

            try:
                if not FileUtils.query_yes_no(f"{prompt}\nDo you want to continue?"):
                    self.log.sysexit_with_message("Aborted...")
            except KeyboardInterrupt:
                self.log.sysexit_with_message("Aborted...")

        for tf in template_files:
            doc_file = os.path.join(
                self.config.config.get("renderer.dest"), os.path.splitext(tf)[0]
            )
            provider, template = self.config.get_template()
            template = os.path.join(template, tf)

            self.logger.debug(
                f"Writing renderer output to: {os.path.relpath(doc_file, self.log.ctx)} "
                f"from: {os.path.dirname(os.path.relpath(template, self.log.ctx))}"
            )

            # make sure the directory exists
            self._create_dir(os.path.dirname(doc_file))

            if os.path.exists(template) and os.path.isfile(template):
                with open(template) as template:
                    data = template.read()
                    if data is not None:
                        try:
                            jenv = Environment(  # nosec
                                loader=FileSystemLoader(self.config.get_template()),
                                lstrip_blocks=True,
                                trim_blocks=True,
                                autoescape=jinja2.select_autoescape(),
                            )
                            jenv.filters["to_nice_yaml"] = self._to_nice_yaml
                            jenv.filters["deep_get"] = self._deep_get
                            jenv.filters["safe_join"] = self._safe_join
                            # keep the old name of the function to not break custom templates.
                            jenv.filters["save_join"] = self._safe_join
                            template_options = self.config.config.get("template.options")
                            data = jenv.from_string(data).render(
                                role_data, role=role_data, options=template_options
                            )
                            if not self.config.config["dry_run"]:
                                with open(doc_file, "wb") as outfile:
                                    outfile.write(header_content.encode("utf-8"))
                                    outfile.write(data.encode("utf-8"))
                                    self.logger.info(f"Writing to: {doc_file}")
                            else:
                                self.logger.info(f"Writing to: {doc_file}")
                        except (
                            jinja2.exceptions.UndefinedError,
                            jinja2.exceptions.TemplateSyntaxError,
                            jinja2.exceptions.TemplateRuntimeError,
                        ) as e:
                            self.log.sysexit_with_message(
                                f"Jinja2 templating error while loading file: '{tf}'\n{e!s}"
                            )
                        except UnicodeEncodeError as e:
                            self.log.sysexit_with_message(
                                f"Unable to print special characters\n{e!s}"
                            )

    def _to_nice_yaml(self, a, indent=4, **kw):
        """Make verbose, human readable yaml."""
        yaml = ruamel.yaml.YAML()
        yaml.indent(mapping=indent, sequence=(indent * 2), offset=indent)
        stream = ruamel.yaml.compat.StringIO()
        yaml.dump(a, stream, **kw)
        return stream.getvalue().rstrip()

    def _deep_get(self, _, dictionary, keys):
        default = None
        return reduce(
            lambda d, key: d.get(key, default) if isinstance(d, dict) else default,
            keys.split("."),
            dictionary,
        )

    @pass_eval_context
    def _safe_join(self, eval_ctx, value, d=""):
        if isinstance(value, str):
            value = [value]

        normalized = jinja2.filters.do_join(eval_ctx, value, d, attribute=None)

        if self.config.config.renderer.autotrim:
            for s in [r" +(\n|\t| )", r"(\n|\t) +"]:
                normalized = re.sub(s, "\\1", normalized)

        return jinja2.filters.do_mark_safe(normalized)

    def render(self):
        self.logger.info(f"Using renderer destination: {self.config.config.get('renderer.dest')}")
        self._write_doc()
