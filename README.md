# ansible-doctor

[![pre-commit](https://img.shields.io/badge/pre--commit-enabled-brightgreen?logo=pre-commit&logoColor=white)](https://github.com/pre-commit/pre-commit)

Annotation based documentation for your Ansible roles

[![Build Status](https://img.shields.io/drone/build/thegeeklab/ansible-doctor?logo=drone)](https://cloud.drone.io/thegeeklab/ansible-doctor)
[![Docker Hub](https://img.shields.io/badge/dockerhub-latest-blue.svg?logo=docker&logoColor=white)](https://hub.docker.com/r/thegeeklab/ansible-doctor)
[![Quay.io](https://img.shields.io/badge/quay-latest-blue.svg?logo=docker&logoColor=white)](https://quay.io/repository/thegeeklab/ansible-doctor)
[![Python Version](https://img.shields.io/pypi/pyversions/ansible-doctor.svg)](https://pypi.org/project/ansible-doctor/)
[![PyPI Status](https://img.shields.io/pypi/status/ansible-doctor.svg)](https://pypi.org/project/ansible-doctor/)
[![PyPI Release](https://img.shields.io/pypi/v/ansible-doctor.svg)](https://pypi.org/project/ansible-doctor/)
[![GitHub contributors](https://img.shields.io/github/contributors/thegeeklab/ansible-doctor)](https://github.com/thegeeklab/ansible-doctor/graphs/contributors)
[![Source: GitHub](https://img.shields.io/badge/source-github-blue.svg?logo=github&logoColor=white)](https://github.com/thegeeklab/ansible-doctor)
[![License: GPL-3.0](https://img.shields.io/github/license/thegeeklab/ansible-doctor)](https://github.com/thegeeklab/ansible-doctor/blob/master/LICENSE)

This project is based on the idea (and at some parts on the code) of [ansible-autodoc](https://github.com/AndresBott/ansible-autodoc) by Andres Bott so credits goes to him for his work.

_ansible-doctor_ is a simple annotation like documentation generator based on Jinja2 templates. While _ansible-doctor_ comes with a default template called `readme`, it is also possible to write your own templates. This gives you the ability to customize the output and render the data to every format you like (e.g. HTML or XML).

_ansible-doctor_ is designed to work within your CI pipeline to complete your testing and deployment workflow. Releases are available as Python Packages on [GitHub](https://github.com/thegeeklab/ansible-doctor/releases) or [PyPI](https://pypi.org/project/ansible-doctor/) and as Docker Image on [Docker Hub](https://hub.docker.com/r/thegeeklab/ansible-doctor).

You can find the full documentation at [https://ansible-doctor.geekdocs.de](https://ansible-doctor.geekdocs.de/).

## Pre-commit hook

~~~bash
pip install pre-commit
# Feel .pre-commit-config.yaml as showed below
pre-commit install
pre-commit run --all-files
~~~

Sample ``.pre-commit-config.yaml``

~~~yaml
-   repo: https://gitlab.com/apollocreed/ansible-doctor
    rev: 1.0.0
    hooks:
      - id: gitlab-ci-linter
~~~

To specify your own ``.ansibledoctor.yml`` file

~~~yaml
-   repo: https://gitlab.com/apollocreed/ansible-doctor
    rev: 1.0.0
    hooks:
      - id: gitlab-ci-linter
        args:
          - -c
          - .ansibledoctor.yml
# You can continue this logic for all argument of CLI
~~~

## Contributors

Special thanks goes to all [contributors](https://github.com/thegeeklab/ansible-doctor/graphs/contributors).

## License

This project is licensed under the GPL-3.0 License - see the [LICENSE](https://github.com/thegeeklab/ansible-doctor/blob/master/LICENSE) file for details.
