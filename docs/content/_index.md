---
title: Documentation
---

[![Build Status](https://img.shields.io/drone/build/thegeeklab/ansible-doctor?logo=drone)](https://cloud.drone.io/thegeeklab/ansible-doctor)
[![Docker Hub](https://img.shields.io/badge/dockerhub-latest-blue.svg?logo=docker&logoColor=white)](https://hub.docker.com/r/thegeeklab/ansible-doctor)
[![Quay.io](https://img.shields.io/badge/quay-latest-blue.svg?logo=docker&logoColor=white)](https://quay.io/repository/thegeeklab/ansible-doctor)
[![Python Version](https://img.shields.io/pypi/pyversions/ansible-doctor.svg)](https://pypi.org/project/ansible-doctor/)
[![PyPI Status](https://img.shields.io/pypi/status/ansible-doctor.svg)](https://pypi.org/project/ansible-doctor/)
[![PyPI Release](https://img.shields.io/pypi/v/ansible-doctor.svg)](https://pypi.org/project/ansible-doctor/)
[![Source: GitHub](https://img.shields.io/badge/source-github-blue.svg?logo=github&logoColor=white)](https://github.com/thegeeklab/ansible-doctor)
[![GitHub contributors](https://img.shields.io/github/contributors/thegeeklab/ansible-doctor)](https://github.com/thegeeklab/ansible-doctor/graphs/contributors)
[![License: GPL-3.0](https://img.shields.io/github/license/thegeeklab/ansible-doctor)](https://github.com/thegeeklab/ansible-doctor/blob/master/LICENSE)

This project is based on the idea (and at some parts on the code) of [ansible-autodoc](https://github.com/AndresBott/ansible-autodoc) by Andres Bott so credits goes to him for his work.

_ansible-doctor_ is a simple annotation like documentation generator based on Jinja2 templates. While _ansible-doctor_ comes with a default template called `readme`, it is also possible to write your own templates. This gives you the ability to customize the output and render the data to every format you like (e.g. HTML or XML).

_ansible-doctor_ is designed to work within your CI pipeline to complete your testing and deployment workflow. Releases are available as Python Packages at [GitHub](https://github.com/thegeeklab/ansible-doctor/releases) or [PyPI](https://pypi.org/project/ansible-doctor/) and as Docker Image at [Docker Hub](https://hub.docker.com/r/thegeeklab/ansible-doctor).
