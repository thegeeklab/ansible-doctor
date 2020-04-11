#!/usr/bin/env python3
"""Find and parse annotations to AnnotationItem objects."""

import json
import re
from collections import defaultdict

import anyconfig

from ansibledoctor.Config import SingleConfig
from ansibledoctor.Utils import SingleLog


class AnnotationItem:
    """Handle annotations."""

    # next time improve this by looping over public available attributes
    def __init__(self):
        self.data = defaultdict(dict)

    def __str__(self):
        """Beautify object string output."""
        for key in self.data.keys():
            for sub in self.data.get(key):
                return "AnnotationItem({}: {})".format(key, sub)

    def get_obj(self):
        return self.data


class Annotation:
    """Handle annotations."""

    def __init__(self, name, files_registry):
        self._all_items = defaultdict(dict)
        self._file_handler = None
        self.config = SingleConfig()
        self.log = SingleLog()
        self.logger = self.log.logger
        self._files_registry = files_registry

        self._all_annotations = self.config.get_annotations_definition()

        if name in self._all_annotations.keys():
            self._annotation_definition = self._all_annotations[name]

        if self._annotation_definition is not None:
            self._find_annotation()

    def get_details(self):
        return self._all_items

    def _find_annotation(self):
        regex = r"(\#\ *\@" + self._annotation_definition["name"] + r"\ +.*)"
        for rfile in self._files_registry.get_files():
            self._file_handler = open(rfile, encoding="utf8")

            num = 1
            while True:
                line = self._file_handler.readline()
                if not line:
                    break

                if re.match(regex, line.strip()):
                    item = self._get_annotation_data(
                        num, line, self._annotation_definition["name"], rfile
                    )
                    if item:
                        self.logger.info(str(item))
                        self._populate_item(item.get_obj().items())
                num += 1

            self._file_handler.close()

    def _populate_item(self, item):
        for key, value in item:
            try:
                anyconfig.merge(self._all_items[key], value, ac_merge=anyconfig.MS_DICTS)
            except ValueError as e:
                self.log.sysexit_with_message("Unable to merge annotation values:\n{}".format(e))

    def _get_annotation_data(self, num, line, name, rfile):
        """
        Make some string conversion on a line in order to get the relevant data.

        :param line:
        """
        item = AnnotationItem()

        # step1 remove the annotation
        reg1 = r"(\#\ *\@" + name + r"\ *)"
        line1 = re.sub(reg1, "", line).strip()

        # step3 take the main key value from the annotation
        parts = [part.strip() for part in line1.split(":", 2)]
        key = str(parts[0])
        item.data[key] = {}
        multiline_char = [">", "$>"]

        if len(parts) < 2:
            return

        if len(parts) == 2:
            parts = parts[:1] + ["value"] + parts[1:]

        subtypes = self.config.ANNOTATIONS.get(name)["subtypes"]
        if subtypes and parts[1] not in subtypes:
            return

        content = [parts[2]]

        if parts[2] not in multiline_char and parts[2].startswith("$"):
            source = parts[2].replace("$", "").strip()
            content = self._str_to_json(key, source, rfile, num, line)

        item.data[key][parts[1]] = content

        # step4 check for multiline description
        if parts[2] in multiline_char:
            multiline = []
            stars_with_annotation = r"(\#\ *[\@][\w]+)"
            current_file_position = self._file_handler.tell()
            newline = ""

            while True:
                next_line = self._file_handler.readline().lstrip()

                if not next_line.strip():
                    self._file_handler.seek(current_file_position)
                    break

                # match if annotation in line
                if re.match(stars_with_annotation, next_line):
                    self._file_handler.seek(current_file_position)
                    break

                # match if does not start with comment
                test_line2 = next_line.strip()
                if test_line2[:1] != "#":
                    self._file_handler.seek(current_file_position)
                    break

                final = re.findall(r"\#(.*)", next_line)[0].rstrip()
                if final[:1] == " ":
                    final = final[1:]
                final = newline + final

                # match if empty line or commented empty line
                test_line = next_line.replace("#", "").strip()
                if len(test_line) == 0:
                    newline = "\n\n"
                    continue
                else:
                    newline = ""

                multiline.append(newline + final)

            if parts[2].startswith("$"):
                source = "".join([x.strip() for x in multiline])
                multiline = self._str_to_json(key, source, rfile, num, line)

            item.data[key][parts[1]] = multiline
        return item

    def _str_to_json(self, key, string, rfile, num, line):
        try:
            return {key: json.loads(string)}
        except ValueError:
            self.log.sysexit_with_message(
                "Json value error: Can't parse json in {}:{}:\n{}".format(
                    rfile, str(num), line.strip()
                )
            )
