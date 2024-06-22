#!/usr/bin/env python3
"""Entrypoint and CLI handler."""

import argparse
import os

import structlog

import ansibledoctor.exception
from ansibledoctor import __version__
from ansibledoctor.config import SingleConfig
from ansibledoctor.doc_generator import Generator
from ansibledoctor.doc_parser import Parser
from ansibledoctor.utils import sysexit_with_message


class AnsibleDoctor:
    """Create main object."""

    log = structlog.get_logger()

    def __init__(self):
        try:
            self.config = SingleConfig()
            self.config.load(args=self._parse_args())
            self._execute()
        except ansibledoctor.exception.DoctorError as e:
            sysexit_with_message(e)
        except FileNotFoundError as e:
            sysexit_with_message("Base directory not found", path=e.filename)
        except KeyboardInterrupt:
            sysexit_with_message("Aborted...")

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

    def _execute(self):
        cwd = os.path.abspath(self.config.config.base_dir)
        walkdirs = [cwd]

        if self.config.config.recursive:
            walkdirs = [f.path for f in os.scandir(cwd) if f.is_dir()]

        for item in walkdirs:
            os.chdir(item)
            self.config.load(root_path=os.getcwd())

            self.log.debug("Switch working directory", path=item)
            self.log.info("Lookup config file", path=self.config.config_files)

            if self.config.config.role.autodetect:
                if self.config.is_role():
                    structlog.contextvars.bind_contextvars(role=self.config.config.role_name)
                    self.log.info("Ansible role detected")
                else:
                    sysexit_with_message("No Ansible role detected")
            else:
                self.log.info("Ansible role detection disabled")

            doc_parser = Parser()
            doc_generator = Generator(doc_parser)
            doc_generator.render()


def main():
    AnsibleDoctor()
