#!/usr/bin/env python3

import argparse
import logging
import os
import sys

from ansibledoctor import __version__
from ansibledoctor.Config import SingleConfig
from ansibledoctor.DocumentationGenerator import Generator
from ansibledoctor.DocumentationParser import Parser
from ansibledoctor.Utils import SingleLog


class AnsibleDoctor:

    def __init__(self):
        self.log = SingleLog()
        self.logger = self.log.logger
        self.args = self._cli_args()
        self.config = self._get_config()

        doc_parser = Parser()
        doc_generator = Generator(doc_parser)
        doc_generator.render()

    def _cli_args(self):
        """
        Use argparse for parsing CLI arguments.

        :return: args objec
        """
        parser = argparse.ArgumentParser(
            description="Generate documentation from annotated Ansible roles using templates")
        parser.add_argument("base_dir", nargs="?", help="role directory, (default: current working dir)")
        parser.add_argument("-c", "--config", nargs="?", help="location of configuration file")
        parser.add_argument("-o", "--output", action="store", dest="output_dir", type=str,
                            help="output base dir")
        parser.add_argument("-f", "--force", action="store_true", dest="force_overwrite",
                            help="force overwrite output file")
        parser.add_argument("-d", "--dry-run", action="store_true", help="dry run without writing")
        # parser.add_argument("-p", "--print", action="store_true",
        #                     help="print to stdout instead of file")
        parser.add_argument("-v", dest="logging.level", action="append_const", const=-1,
                            help="increase log level")
        parser.add_argument("-q", dest="logging.level", action="append_const",
                            const=1, help="decrease log level")
        parser.add_argument("--version", action="version", version="%(prog)s {}".format(__version__))

        return parser.parse_args().__dict__

    def _get_config(self):
        config = SingleConfig(args=self.args)
        if config.is_role:
            self.logger.info("Ansible role detected")
        else:
            self.log.error("No Ansible role detected")
            sys.exit(1)

        # TODO: user wrapper method to catch config exceptions
        return config
