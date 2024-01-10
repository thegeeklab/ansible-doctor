---
title: Using pip
---

```Shell
# From PyPI as unprivileged user
$ pip install ansible-doctor[ansible-core] --user

# .. or as root
$ sudo pip install ansible-doctor[ansible-core]

# From Wheel file
# Please check first whether a newer version is available.
$ pip install https://github.com/thegeeklab/ansible-doctor/releases/download/v3.1.4/ansible_doctor-3.1.4-py2.py3-none-any.whl[ansible-core]
```
