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
role_dir:
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
template_src:
template: readme

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
usage: ansible-doctor [-h] [-c CONFIG_FILE] [-o OUTPUT_DIR] [-f] [-d] [-n] [-v] [-q] [--version] [role_dir]

Generate documentation from annotated Ansible roles using templates

positional arguments:
  role_dir              role directory (default: current working dir)

optional arguments:
  -h, --help            show this help message and exit
  -c CONFIG_FILE, --config CONFIG_FILE
                        location of configuration file
  -o OUTPUT_DIR, --output OUTPUT_DIR
                        output base dir
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
ANSIBLE_DOCTOR_ROLE_DIR=
ANSIBLE_DOCTOR_ROLE_NAME=
ANSIBLE_DOCTOR_DRY_RUN=false
ANSIBLE_DOCTOR_LOG_LEVEL=warning
ANSIBLE_DOCTOR_LOG_JSON=false
ANSIBLE_DOCTOR_OUTPUT_DIR=
ANSIBLE_DOCTOR_TEMPLATE_SRC=
ANSIBLE_DOCTOR_TEMPLATE=readme
ANSIBLE_DOCTOR_FORCE_OVERWRITE=false
ANSIBLE_DOCTOR_CUSTOM_HEADER=
ANSIBLE_DOCTOR_EXCLUDE_FILES=
ANSIBLE_DOCTOR_EXCLUDE_FILES=molecule/,files/**/*.py
```
