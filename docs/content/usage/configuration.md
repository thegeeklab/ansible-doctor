---
title: Configuration
---

_ansible-doctor_ comes with default settings which should be sufficient for most users to start, but most of the settings can be adjusted.

{{< toc >}}

Configuration options can be set in different places, which are processed in the following order (last wins):

- Standard configuration (built-in)
- Global configuration file (the path depends on the operating system)
- Folder-based configuration file (`.ansibledoctor.yml|.ansibledoctor.yaml|.ansibledoctor`) in the current working directory
- Environment Variables
- CLI options

## Defaults

```YAML
---
# Default is the current working directory.
base_dir:
# Default is the basename of 'role_name'.
role_name:
# Auto-detect if the given directory is a role, can be disabled
# to parse loose files instead.
role_detection: True
# Don't write anything to file system
dry_run: False

logging:
    # Possible options debug | info | warning | error | critical
    level: "warning"
    # Json logging can be enabled if a parsable output is required
    json: False

# Path to write rendered template file. Default is the current working directory.
output_dir:
# Default is built-in templates directory.
template_dir:
template: readme
# By default, double spaces, spaces before and after line breaks or tab characters, etc.
# are automatically removed before the template is rendered. As a result, indenting
# with spaces does not work. If you want to use spaces to indent text, you must disable
# this option.
template_autotrim: True

# Don't ask to overwrite if output file exists.
force_overwrite: False
# Load custom header from given file and append template output to it before write.
custom_header: ""

exclude_files: []
# Examples
# exclude_files:
#   - molecule/
#   - files/**/*.py

# Exclude tags from automatic detection. Configured tags are only skipped
# if the tag is not used in an annotation.
exclude_tags: []
```

## CLI

```Shell
$ ansible-doctor --help
usage: ansible-doctor [-h] [-c CONFIG_FILE] [-o OUTPUT_DIR] [-r] [-f] [-d] [-n] [-v] [-q] [--version] [base_dir]

Generate documentation from annotated Ansible roles using templates

positional arguments:
  base_dir              base directory (default: current working directory)

options:
  -h, --help            show this help message and exit
  -c CONFIG_FILE, --config CONFIG_FILE
                        path to configuration file
  -o OUTPUT_DIR, --output OUTPUT_DIR
                        output directory
  -r, --recursive       run recursively over the base directory subfolders
  -f, --force           force overwrite output file
  -d, --dry-run         dry run without writing
  -n, --no-role-detection
                        disable automatic role detection
  -v                    increase log level
  -q                    decrease log level
  --version             show program's version number and exit
```

## Environment Variables

```Shell
ANSIBLE_DOCTOR_CONFIG_FILE=
ANSIBLE_DOCTOR_ROLE_DETECTION=true
ANSIBLE_DOCTOR_BASE_DIR=
ANSIBLE_DOCTOR_RECURSIVE=false
ANSIBLE_DOCTOR_ROLE_NAME=
ANSIBLE_DOCTOR_DRY_RUN=false
ANSIBLE_DOCTOR_LOG_LEVEL=warning
ANSIBLE_DOCTOR_LOG_JSON=false
ANSIBLE_DOCTOR_OUTPUT_DIR=
ANSIBLE_DOCTOR_TEMPLATE_DIR=
ANSIBLE_DOCTOR_TEMPLATE=readme
ANSIBLE_DOCTOR_TEMPLATE_AUTOTRIM=true
ANSIBLE_DOCTOR_FORCE_OVERWRITE=false
ANSIBLE_DOCTOR_CUSTOM_HEADER=
ANSIBLE_DOCTOR_EXCLUDE_FILES=
ANSIBLE_DOCTOR_EXCLUDE_FILES=molecule/,files/**/*.py
```

## Pre-Commit setup

To use _ansible-doctor_ with the [pre-commit](https://pre-commit.com/) framework, add the following to the `.pre-commit-config.yaml` file in your local repository.

<!-- prettier-ignore-start -->
<!-- markdownlint-disable -->
<!-- spellchecker-disable -->

{{< highlight yaml "linenos=table" >}}
- repo: https://github.com/thegeeklab/ansible-doctor
  # change ref to the latest release from https://github.com/thegeeklab/ansible-doctor/releases
  rev: v1.4.8
  hooks:
    - id: ansible-doctor
{{< /highlight >}}

<!-- spellchecker-enable -->
<!-- markdownlint-restore -->
<!-- prettier-ignore-end -->
