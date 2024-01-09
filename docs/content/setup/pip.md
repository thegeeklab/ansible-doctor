---
title: Using pip
---

```Shell
# From PyPI as unprivileged user
$ pip install ansible-doctor[ansible-core] --user

# .. or as root
$ sudo pip install ansible-doctor[ansible-core]

# From Wheel file
$ pip install https://github.com/thegeeklab/ansible-doctor/releases/download/v0.1.1/ansible_doctor-0.1.1-py2.py3-none-any.whl[ansible-core]
```
