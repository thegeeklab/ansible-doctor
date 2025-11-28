"""Utils for YAML file operations."""

from collections import defaultdict
from contextlib import suppress
from io import StringIO, TextIOBase
from typing import Any

import ruamel.yaml
import yaml
from ansible.parsing.yaml.loader import AnsibleLoader
from ruamel.yaml.constructor import SafeConstructor

import ansibledoctor.exception


class UnsafeTag:
    """Handle custom yaml unsafe tag."""

    yaml_tag = "!unsafe"

    def __init__(self, value: str) -> None:
        self.unsafe: str = value

    @staticmethod
    def yaml_constructor(loader: yaml.SafeLoader, node: object) -> Any:
        return loader.construct_scalar(node)


def parse_yaml_ansible(
    yaml_file: TextIOBase | StringIO | str,
) -> list[Any] | dict[Any, Any]:
    try:
        loader = AnsibleLoader(yaml_file)
        data = loader.get_single_data() or []
    except (
        yaml.parser.ParserError,
        yaml.scanner.ScannerError,
        yaml.constructor.ConstructorError,
        yaml.composer.ComposerError,
    ) as e:
        raise ansibledoctor.exception.YAMLError(e) from e

    return data


def parse_yaml(yaml_file: TextIOBase | StringIO | str) -> dict[Any, Any]:
    try:
        ruamel.yaml.add_constructor(
            UnsafeTag.yaml_tag,
            UnsafeTag.yaml_constructor,
            constructor=SafeConstructor,
        )

        data = ruamel.yaml.YAML(typ="rt").load(yaml_file)
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


def _yaml_remove_comments(d: dict[Any, Any] | list[Any] | Any) -> None:
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
