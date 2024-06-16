"""Utils for YAML file operations."""

from collections import defaultdict
from contextlib import suppress

import ruamel.yaml
import yaml
from ansible.parsing.yaml.loader import AnsibleLoader

import ansibledoctor.exception


class UnsafeTag:
    """Handle custom yaml unsafe tag."""

    yaml_tag = "!unsafe"

    def __init__(self, value):
        self.unsafe = value

    @staticmethod
    def yaml_constructor(loader, node):
        return loader.construct_scalar(node)


def parse_yaml_ansible(yamlfile):
    try:
        loader = AnsibleLoader(yamlfile)
        data = loader.get_single_data() or []
    except (
        yaml.parser.ParserError,
        yaml.scanner.ScannerError,
        yaml.constructor.ConstructorError,
        yaml.composer.ComposerError,
    ) as e:
        raise ansibledoctor.exception.YAMLError(e) from e

    return data


def parse_yaml(yamlfile):
    try:
        ruamel.yaml.add_constructor(
            UnsafeTag.yaml_tag,
            UnsafeTag.yaml_constructor,
            constructor=ruamel.yaml.SafeConstructor,
        )

        data = ruamel.yaml.YAML(typ="rt").load(yamlfile)
        _yaml_remove_comments(data)
        data = defaultdict(dict, data or {})
    except (
        ruamel.yaml.parser.ParserError,
        ruamel.yaml.scanner.ScannerError,
        ruamel.yaml.constructor.ConstructorError,
        ruamel.yaml.composer.ComposerError,
    ) as e:
        raise ansibledoctor.exception.YAMLError(e) from e

    return data


def _yaml_remove_comments(d):
    if isinstance(d, dict):
        for k, v in d.items():
            _yaml_remove_comments(k)
            _yaml_remove_comments(v)
    elif isinstance(d, list):
        for elem in d:
            _yaml_remove_comments(elem)

    with suppress(AttributeError):
        attr = (
            "comment"
            if isinstance(d, ruamel.yaml.scalarstring.ScalarString)
            else ruamel.yaml.comments.Comment.attrib
        )
        delattr(d, attr)
