# ansible-doctor

ansible-doctor - Simple annotation based documentation for your roles

[![Build Status](https://img.shields.io/drone/build/xoxys/ansible-doctor?logo=drone)](https://cloud.drone.io/xoxys/ansible-doctor)
[![Docker Hub](https://img.shields.io/badge/docker-latest-blue.svg?logo=docker&logoColor=white)](https://hub.docker.com/r/xoxys/ansible-doctor)
[![Python Version](https://img.shields.io/pypi/pyversions/ansible-doctor.svg)](https://pypi.org/project/ansible-doctor/)
[![PyPI Status](https://img.shields.io/pypi/status/ansible-doctor.svg)](https://pypi.org/project/ansible-doctor/)
[![PyPI Release](https://img.shields.io/pypi/v/ansible-doctor.svg)](https://pypi.org/project/ansible-doctor/)
[![License: MIT](https://img.shields.io/github/license/xoxys/ansible-doctor)](LICENSE)

This project is based on the idea (and at some parts on the code) of [ansible-autodoc](https://github.com/AndresBott/ansible-autodoc) by Andres Bott so credits goes to him for his work.

_ansible-doctor_ is a simple annotation like documentation generator based on Jinja2 templates. While _ansible-doctor_ comes with a default template called `readme`, it is also possible to write your own templates. This gives you the ability to customize the output and render the data to every format you like (e.g. HTML or XML).

_ansible-doctor_ is designed to work within your CI pipeline to complete your testing and deployment workflow. Releases are available as Python Packages on [GitHub](https://github.com/xoxys/ansible-doctor/releases) or [PyPI](https://pypi.org/project/ansible-doctor/) and as Docker Image on [Docker Hub](https://hub.docker.com/r/xoxys/ansible-doctor).

You can find the full documentation at [https://ansible-doctor.geekdocs.de](https://ansible-doctor.geekdocs.de/).

## License

This project is licensed under the GNU v3.0 - see the [LICENSE](https://github.com/xoxys/ansible-doctor/blob/master/LICENSE) file for details.

## Maintainers and Contributors

[Robert Kaussow](https://github.com/xoxys)
