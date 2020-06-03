---
title: Using pip

---

<!-- markdownlint-disable -->
{{< highlight Shell "linenos=table" >}}
# From PyPI as unprivileged user
$ pip install ansible-doctor --user

# .. or as root
$ sudo pip install ansible-doctor

# From Wheel file
$ pip install https://github.com/xoxys/ansible-doctor/releases/download/v0.1.1/ansible_doctor-0.1.1-py2.py3-none-any.whl
{{< /highlight >}}
<!-- markdownlint-restore -->
