#!/usr/bin/env python3

import argparse
import os
import sys

from ansibledoctor import __version__
from ansibledoctor.Config import SingleConfig
from ansibledoctor.DocumentationGenerator import Generator
from ansibledoctor.DocumentationParser import Parser
from ansibledoctor.Utils import SingleLog


class AnsibleDoctor:

    def __init__(self):
        self.config = SingleConfig()
        self.log = SingleLog(self.config.debug_level)
        args = self._cli_args()
        self._parse_args(args)

        doc_parser = Parser()
        doc_generator = Generator(doc_parser)
        doc_generator.render()

    def _cli_args(self):
        """
        Use argparse for parsing CLI arguments.

        :return: args objec
        """
        parser = argparse.ArgumentParser(
            description="Generate documentation from annotated playbooks and roles using templates")
        parser.add_argument("project_dir", nargs="?", default=os.getcwd(),
                            help="role directory, (default: current working dir)")
        parser.add_argument("-c", "--conf", nargs="?", default="",
                            help="location of configuration file")
        parser.add_argument("-o", "--output", action="store", dest="output", type=str,
                            help="output base dir")
        parser.add_argument("-f", "--force", action="store_true", help="force overwrite output file")
        parser.add_argument("-d", "--dry-run", action="store_true", help="dry run without writing")
        parser.add_argument("-D", "--default", action="store_true", help="print the default configuration")
        parser.add_argument("-p", "--print", nargs="?", default="_unset_",
                            help="use print template instead of writing to files")
        parser.add_argument("--version", action="version", version="%(prog)s {}".format(__version__))

        debug_level = parser.add_mutually_exclusive_group()
        debug_level.add_argument("-v", action="store_true", help="Set debug level to info")
        debug_level.add_argument("-vv", action="store_true", help="Set debug level to debug")
        debug_level.add_argument("-vvv", action="store_true", help="Set debug level to trace")

        return parser.parse_args()

    def _parse_args(self, args):
        """
        Use an args object to apply all the configuration combinations to the config object.

        :param args:
        :return: None
        """
        self.config.set_base_dir(os.path.abspath(args.project_dir))

        # search for config file
        if args.conf != "":
            conf_file = os.path.abspath(args.conf)
            if os.path.isfile(conf_file) and os.path.basename(conf_file) == self.config.config_file_name:
                self.config.load_config_file(conf_file)
                # re apply log level based on config
                self.log.set_level(self.config.debug_level)
            else:
                self.log.warn("No configuration file found: " + conf_file)
        else:
            conf_file = self.config.get_base_dir() + "/" + self.config.config_file_name
            if os.path.isfile(conf_file):
                self.config.load_config_file(conf_file)
                # re apply log level based on config
                self.log.set_level(self.config.debug_level)

        # sample configuration
        if args.default:
            print(self.config.sample_config)
            sys.exit()

        # Debug levels
        if args.v is True:
            self.log.set_level("info")
        elif args.vv is True:
            self.log.set_level("debug")
        elif args.vvv is True:
            self.log.set_level("trace")

        # need to send the message after the log levels have been set
        self.log.debug("using configuration file: " + conf_file)

        # Overwrite
        if args.force is True:
            self.config.template_overwrite = True

        # Dry run
        if args.dry_run is True:
            self.config.dry_run = True
            if self.log.log_level > 1:
                self.log.set_level(1)
                self.log.info("Running in Dry mode: Therefore setting log level at least to INFO")

        # Print template
        if args.print == "_unset_":
            pass
        elif args.print is None:
            self.config.use_print_template = "all"
        else:
            self.config.use_print_template = args.print

        # output dir
        if args.output is not None:
            self.config.output_dir = os.path.abspath(args.output)

        # some debug
        self.log.debug(args)
        self.log.info("Using base dir: " + self.config.get_base_dir())

        if self.config.is_role:
            self.log.info("This is detected as: ROLE ")
        elif self.config.is_role is not None and not self.config.is_role:
            self.log.info("This is detected as: PLAYBOOK ")
        else:
            self.log.error([
                self.config.get_base_dir() + "/tasks"
            ], "No ansible role detected, checked for: ")
            sys.exit(1)
