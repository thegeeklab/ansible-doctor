# ansible-doctor

Annotation based documentation for your Ansible roles

[![Build Status](https://ci.thegeeklab.de/api/badges/thegeeklab/ansible-doctor/status.svg)](https://ci.thegeeklab.de/repos/thegeeklab/ansible-doctor)
[![Docker Hub](https://img.shields.io/badge/dockerhub-latest-blue.svg?logo=docker&logoColor=white)](https://hub.docker.com/r/thegeeklab/ansible-doctor)
[![Quay.io](https://img.shields.io/badge/quay-latest-blue.svg?logo=docker&logoColor=white)](https://quay.io/repository/thegeeklab/ansible-doctor)
[![Python Version](https://img.shields.io/pypi/pyversions/ansible-doctor.svg)](https://pypi.org/project/ansible-doctor/)
[![PyPI Status](https://img.shields.io/pypi/status/ansible-doctor.svg)](https://pypi.org/project/ansible-doctor/)
[![PyPI Release](https://img.shields.io/pypi/v/ansible-doctor.svg)](https://pypi.org/project/ansible-doctor/)
[![GitHub contributors](https://img.shields.io/github/contributors/thegeeklab/ansible-doctor)](https://github.com/thegeeklab/ansible-doctor/graphs/contributors)
[![Source: GitHub](https://img.shields.io/badge/source-github-blue.svg?logo=github&logoColor=white)](https://github.com/thegeeklab/ansible-doctor)
[![License: GPL-3.0](https://img.shields.io/github/license/thegeeklab/ansible-doctor)](https://github.com/thegeeklab/ansible-doctor/blob/main/LICENSE)

This project is based on the idea (and at some parts on the code) of [ansible-autodoc](https://github.com/AndresBott/ansible-autodoc) by Andres Bott so credits goes to him for his work.

_ansible-doctor_ is a simple annotation like documentation generator based on Jinja2 templates. While _ansible-doctor_ comes with a default template called `readme`, it is also possible to write custom templates to customize the output or render the data to other formats like HTML or XML as well.

_ansible-doctor_ is designed to work within a CI pipeline to complete the existing testing and deployment workflow. Releases are available as Python Packages on [GitHub](https://github.com/thegeeklab/ansible-doctor/releases) or [PyPI](https://pypi.org/project/ansible-doctor/) and as Docker Image on [Docker Hub](https://hub.docker.com/r/thegeeklab/ansible-doctor).

The full documentation is available at [https://ansible-doctor.geekdocs.de](https://ansible-doctor.geekdocs.de/).

## Contributors

Special thanks to all [contributors](https://github.com/thegeeklab/ansible-doctor/graphs/contributors). If you would like to contribute,
please see the [instructions](https://github.com/thegeeklab/ansible-doctor/blob/main/CONTRIBUTING.md).

## License

This project is licensed under the GPL-3.0 License - see the [LICENSE](https://github.com/thegeeklab/ansible-doctor/blob/main/LICENSE) file for details.
