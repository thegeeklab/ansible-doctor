# ansible-doctor

[![Build Status](https://cloud.drone.io/api/badges/xoxys/ansible-doctor/status.svg)](https://cloud.drone.io/xoxys/ansible-doctor)
[![](https://images.microbadger.com/badges/image/xoxys/ansible-doctor.svg)](https://microbadger.com/images/xoxys/ansible-doctor "Get your own image badge on microbadger.com")
[![](https://img.shields.io/pypi/pyversions/ansible-doctor.svg)](https://pypi.org/project/ansible-doctor/)
[![](https://img.shields.io/pypi/status/ansible-doctor.svg)](https://pypi.org/project/ansible-doctor/)
[![](https://img.shields.io/pypi/v/ansible-doctor.svg)](https://pypi.org/project/ansible-doctor/)
![License](https://img.shields.io/github/license/xoxys/ansible-doctor)

This project is based on the idea (and at some parts on the code) of [ansible-autodoc](https://github.com/AndresBott/ansible-autodoc) by Andres Bott so credits goes to him for his work.

`ansible-doctor` is a simple annotation like documentation generator based on Jinja2 templates. While `ansible-doctor` comes with a default template called `readme`, it is also possible to write your own templates. This gives you the ability to customize the output and render the data to every format you like (e.g. html or xml).

`ansible-doctor` is designed to work within your CI pipeline to complete your testing and deployment workflow. Releases are available as Python Packages on [GitHub](https://github.com/xoxys/ansible-doctor/releases) or [PyPI](https://pypi.org/project/ansible-doctor/) and as Docker Image on [DockerHub](https://hub.docker.com/r/xoxys/ansible-doctor).

## Table of Content

* [Setup](#Setup)
  * [Using pip](#Using-pip)
  * [Using docker](#Using-docker)
* [Configuration](#Configuration)
  * [Default settings](#Default-settings)
  * [CLI options](#CLI-options)
  * [Environment variables](#Environment-variables)
* [Usage](#Usage)
* [License](#License)
* [Maintainers and Contributors](#Maintainers-and-Contributors)

---

### Setup

#### Using pip

```Shell
# From PyPI as unprivilegd user
$ pip install ansible-doctor --user

# .. or as root
$ sudo pip install ansible-doctor

# From Wheel file
$ pip install https://github.com/xoxys/ansible-doctor/releases/download/v0.1.1/ansible_doctor-0.1.1-py2.py3-none-any.whl
```

#### Using docker

```Shell
docker run \
    -e ANSIBLE_DOCTOR_ROLE_DIR=example/demo-role/ \
    -e ANSIBLE_DOCTOR_OUTPUT_DIR=example/ \
    -e ANSIBLE_DOCTOR_FORCE_OVERWRITE=true \
    -e ANSIBLE_DOCTOR_CUSTOM_HEADER=example/demo-role/HEADER.md \
    -e ANSIBLE_DOCTOR_LOG_LEVEL=info \
    -e PY_COLORS=1 \
    -v $(pwd):/doctor \
    -w /doctor \
    xoxys/ansible-doctor
```

Keep in mind, that you have to pass selinux labels (:Z or :z) to your mount option if you are working on a selinux enabled system.

### Configuration

`ansible-doctor` comes with default settings which should be sufficient for most users to start, but you can adjust most settings to your needs.

Changes can be made on different locations which will be processed in the following order (last wins):

* default config (build-in)
* global config file (path depends on your operating system)
* folder-based config file (.ansibledoctor.yml|.ansibledoctor.yaml|.ansibledoctor in current working dir)
* environment variables
* cli options

#### Default settings

```YAML
---
# default is your current working dir
role_dir:
# don't write anything to filesystem
dry_run: False

logging:
    # possible options debug | info | warning | error | critical
    level: "warning"
    # you can enable json logging if a parsable output is required
    json: False

# path to write rendered template file
# default is your current working dir
output_dir:
# default is in-build templates dir
template_dir:
template: readme

# don't ask to overwrite if output file exists
force_overwrite: False
# load custom header from given file and append template output
# to it before write.
custom_header: ""

exclude_files: []
# Examples
# exclude_files:
#   - molecule/
#   - files/**/*.py
```

#### CLI options

```Shell
$ ansible-doctor --help
usage: ansible-doctor [-h] [-c CONFIG_FILE] [-o OUTPUT_DIR] [-f] [-d] [-v]
                      [-q] [--version]
                      role_dir

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
  -v                    increase log level
  -q                    decrease log level
  --version             show program's version number and exit
```

#### Environment variables

```Shell
ANSIBLE_DOCTOR_CONFIG_FILE=
ANSIBLE_DOCTOR_ROLE_DIR=
ANSIBLE_DOCTOR_DRY_RUN=false
ANSIBLE_DOCTOR_LOG_LEVEL=warning
ANSIBLE_DOCTOR_LOG_JSON=false
ANSIBLE_DOCTOR_OUTPUT_DIR=
ANSIBLE_DOCTOR_TEMPLATE_DIR=
ANSIBLE_DOCTOR_TEMPLATE=readme
ANSIBLE_DOCTOR_FORCE_OVERWRITE=false
ANSIBLE_DOCTOR_CUSTOM_HEADER=
ANSIBLE_DOCTOR_EXCLUDE_FILES=
# ANSIBLE_DOCTOR_EXCLUDE_FILES=molecule/,files/**/*.py
```

### Usage

```Shell
ansible-doctor FOLDER
```

If you don't pass a folder to `ansible-doctor` your current working directory will be used. The first step is to identify if the given folder is an ansible role. This check is very simple, if the folder contains a subfolder called `tasks` is MUST be an ansible role! :)

After the successful check, `ansible-doctor` will try to read some static files into a dictionary:

* defaults/main.yml
* meta/main.yml

This will be the base result set which is used as data source for every output template. Without any work, you will get at least a documentation about available variables and some meta information. Theses basic information can be expanded with a set of available annotations. In general, an annotation is a comment with an identifier. This identifier is followed by colon separated options and ends with a value.

```Yaml
# @identifier option1:option2: <value>

# @var docker_registry_password:example: "%8gv_5GA?"
# @var docker_registry_password:description: Very secure password to login to the docker registry
# @var docker_registry_password:description: >
# You can also write it as multiline description
# Very secure password to login to the docker registry.
# @end
docker_registry_password: "secret"
```

These list of pre-defined identifiers is currently available:

* @meta
* @todo
* @var
* @tag

### License

This project is licensed under the GNU v3.0 - see the [LICENSE](https://github.com/xoxys/ansible-doctor/blob/master/LICENSE) file for details.

### Maintainers and Contributors

[Robert Kaussow](https://github.com/xoxys)
