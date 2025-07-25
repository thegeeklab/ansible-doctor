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

role:
  # Default is the basename of 'role_name'.
  name:
  # Auto-detect if the given directory is a role, can be disabled
  # to parse loose files instead.
  autodetect: True

# Don't write anything to file system.
dry_run: False

exclude_files: []
# Examples
# exclude_files:
#   - molecule/
#   - files/**/*.py

# Exclude tags from automatic detection. Configured tags are only skipped
# if the tag is not used in an annotation.
exclude_tags: []

logging:
  # Possible options: debug|info|warning| error|critical
  level: "warning"
  # JSON logging can be enabled if a parsable output is required.
  json: False

template:
  # Name of the template to be used. In most cases, this is the name of a directory that is attached to the
  # the `src` path or Git repo (see example below).
  name: readme

  # Template provider source. Currently supported providers are `local|git`.
  # The `local` provider loads templates from the local file system. This provider
  # is used by default and uses the built-in templates.
  #
  # Examples:
  # template:
  #   name: readme
  #   src: local>/tmp/custom_templates/
  #
  # The `git` provider allows templates to be loaded from a git repository. At the moment
  # the functions of this provider are limited and only public repositories are supported.
  #
  # Examples:
  # template:
  #   src: git>https://github.com/thegeeklab/ansible-doctor
  #   name: ansibledoctor/templates/readme
  #
  # template:
  #   src: git>git@github.com:thegeeklab/ansible-doctor.git
  #   name: ansibledoctor/templates/readme
  #
  # template:
  #   src: git>git@github.com:thegeeklab/ansible-doctor.git#branch-or-tag
  #   name: ansibledoctor/templates/readme
  src:

  options:
    # Configures whether to tabulate variables in the output. When set to `True`,
    # variables will be displayed in a tabular format instead of plain markdown sections.
    # NOTE: This option does not support rendering multiline code blocks.
    tabulate_vars: False

renderer:
  # By default, double spaces, spaces before and after line breaks or tab characters, etc.
  # are automatically removed before the template is rendered. As a result, indenting
  # with spaces does not work. If you want to use spaces to indent text, you must disable
  # this option.
  autotrim: True
  # Load custom header from given file and append template output to it before write.
  include_header: ""
  # Output path (file or directory). If a directory, the filename is derived from the template name.
  dest:
  # Don't ask to overwrite if output file exists.
  force_overwrite: False

# Define custom subtypes for annotations. To use custom subtypes a custom template is required.
annotations:
  var:
    subtypes: ["custom", "another_custom"]
  tag:
    subtypes: ["custom_field"]
```

## CLI

```Shell
$ ansible-doctor --help
usage: ansible-doctor [-h] [-c CONFIG_FILE] [-o OUTPUT_PATH] [-r] [-f] [-d] [-n] [-v] [-q] [--version] [base_dir]

Generate documentation from annotated Ansible roles using templates

positional arguments:
  base_dir              base directory (default: current working directory)

options:
  -h, --help            show this help message and exit
  -c CONFIG_FILE, --config CONFIG_FILE
                        path to configuration file
  -o OUTPUT_PATH, --output OUTPUT_PATH
                        output file or directory
  -r, --recursive       run recursively over the base directory
  -f, --force           force overwrite output file
  -d, --dry-run         dry run without writing
  -n, --no-role-detection
                        disable automatic role detection
  -v                    increase log level
  -q                    decrease log level
  --version             show program's version number and exit
```

### Output Examples

The `--output` option accepts both files and directories:

```Shell
# Output to specific file
ansible-doctor -o DOCUMENTATION.md

# Output to directory (filename derived from template)
ansible-doctor -o /path/to/docs/

# Output to current directory (default behavior)
ansible-doctor
```

## Environment Variables

{{< hint type=note >}}
List configuration options need to be passed as JSON strings.
{{< /hint >}}

```Shell
ANSIBLE_DOCTOR_BASE_DIR=
ANSIBLE_DOCTOR_DRY_RUN=False
ANSIBLE_DOCTOR_EXCLUDE_FILES="['molecule/']"
ANSIBLE_DOCTOR_EXCLUDE_TAGS="[]"

ANSIBLE_DOCTOR_ROLE__NAME=
ANSIBLE_DOCTOR_ROLE__AUTODETECT=True

ANSIBLE_DOCTOR_LOGGING__LEVEL="warning"
ANSIBLE_DOCTOR_LOGGING__JSON=False

ANSIBLE_DOCTOR_TEMPLATE__NAME=readme
ANSIBLE_DOCTOR_TEMPLATE__SRC=
ANSIBLE_DOCTOR_TEMPLATE__OPTIONS__TABULATE_VARS=False

ANSIBLE_DOCTOR_RENDERER__AUTOTRIM=True
ANSIBLE_DOCTOR_RENDERER__INCLUDE_HEADER=
ANSIBLE_DOCTOR_RENDERER__DEST=
ANSIBLE_DOCTOR_RENDERER__FORCE_OVERWRITE=False

ANSIBLE_DOCTOR_ANNOTATIONS__VAR__SUBTYPES=custom,another_custom
ANSIBLE_DOCTOR_ANNOTATIONS__TAG__SUBTYPES=custom_field
```

## Pre-Commit setup

To use _ansible-doctor_ with the [pre-commit](https://pre-commit.com/) framework, add the following to the `.pre-commit-config.yaml` file in your local repository.

<!-- prettier-ignore-start -->
<!-- markdownlint-disable -->
<!-- spellchecker-disable -->

{{< highlight yaml "linenos=table" >}}
- repo: https://github.com/thegeeklab/ansible-doctor
  # update version with `pre-commit autoupdate`
  rev: v4.0.4
  hooks:
    - id: ansible-doctor
{{< /highlight >}}

<!-- spellchecker-enable -->
<!-- markdownlint-restore -->
<!-- prettier-ignore-end -->
