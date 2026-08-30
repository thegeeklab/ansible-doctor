"""Provide version information."""

import sys
from importlib.metadata import PackageNotFoundError, version

try:
    __version__ = version("ansible-doctor")
except PackageNotFoundError:
    __version__ = "0.0.0"

try:
    import ansible  # noqa
except ImportError:
    sys.exit("ERROR: Python requirements are missing: 'ansible-core' not found.")
