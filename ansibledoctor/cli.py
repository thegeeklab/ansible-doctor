#!/usr/bin/env python3
"""Entrypoint and CLI handler."""

import argparse
import os

import ansibledoctor.exception
from ansibledoctor import __version__
from ansibledoctor.config import SingleConfig
from ansibledoctor.doc_generator import Generator
from ansibledoctor.doc_parser import Parser
from ansibledoctor.utils import SingleLog


class AnsibleDoctor:
    """Create main object."""

    def __init__(self):
        self.log = SingleLog()
        self.logger = self.log.logger
        self._get_config()
        self._execute()

    def _parse_args(self):
        """
        Use argparse for parsing CLI arguments.

        :return: args objec
        """
        # TODO: add function to print to stdout instead of file
        parser = argparse.ArgumentParser(
            description="Generate documentation from annotated Ansible roles using templates"
        )
        parser.add_argument(
            "base_dir",
            nargs="?",
            default=self.config.config.base_dir,
            help="base directory (default: current working directory)",
        )
        parser.add_argument(
            "-c",
            "--config",
            dest="config_file",
            help="path to configuration file",
        )
        parser.add_argument(
            "-o",
            "--output",
            dest="renderer__dest",
            action="store",
            default=self.config.config.renderer.dest,
            help="output directory",
            metavar="OUTPUT_DIR",
        )
        parser.add_argument(
            "-r",
            "--recursive",
            dest="recursive",
            action="store_true",
            default=self.config.config.recursive,
            help="run recursively over the base directory subfolders",
        )
        parser.add_argument(
            "-f",
            "--force",
            dest="renderer.force_overwrite",
            action="store_true",
            default=self.config.config.renderer.force_overwrite,
            help="force overwrite output file",
        )
        parser.add_argument(
            "-d",
            "--dry-run",
            dest="dry_run",
            action="store_true",
            default=self.config.config.dry_run,
            help="dry run without writing",
        )
        parser.add_argument(
            "-n",
            "--no-role-detection",
            dest="role_detection",
            action="store_false",
            default=self.config.config.role.autodetect,
            help="disable automatic role detection",
        )
        parser.add_argument(
            "-v",
            dest="logging.level",
            action="append_const",
            const=-1,
            help="increase log level",
        )
        parser.add_argument(
            "-q",
            dest="logging.level",
            action="append_const",
            const=1,
            help="decrease log level",
        )
        parser.add_argument(
            "--version",
            action="version",
            version=f"%(prog)s {__version__}",
        )

        return parser.parse_args().__dict__

    def _get_config(self):
        try:
            self.config = SingleConfig()
            self.config.load(args=self._parse_args())
            self.log.register_hanlers(json=self.config.config.logging.json)
        except ansibledoctor.exception.ConfigError as e:
            self.log.sysexit_with_message(e)

    def _execute(self):
        cwd = os.path.abspath(self.config.config.base_dir)
        walkdirs = [cwd]

        if self.config.config.recursive:
            walkdirs = [f.path for f in os.scandir(cwd) if f.is_dir()]

        for item in walkdirs:
            os.chdir(item)

            try:
                self.config.load(root_path=os.getcwd())
            except ansibledoctor.exception.ConfigError as e:
                self.log.sysexit_with_message(e)

            try:
                self.log.set_level(self.config.config.logging.level)
            except ValueError as e:
                self.log.sysexit_with_message(f"Can not set log level.\n{e!s}")
            self.logger.info(f"Using config file: {self.config.config_files}")

            self.logger.debug(f"Using working directory: {os.path.relpath(item, self.log.ctx)}")

            if self.config.config.role.autodetect:
                if self.config.is_role():
                    self.logger.info(f"Ansible role detected: {self.config.config.role_name}")
                else:
                    self.log.sysexit_with_message("No Ansible role detected")
            else:
                self.logger.info("Ansible role detection disabled")

            doc_parser = Parser()
            doc_generator = Generator(doc_parser)
            doc_generator.render()


def main():
    AnsibleDoctor()
