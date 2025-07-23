---
title: Using docker
---

```Shell
docker run \
    -e ANSIBLE_DOCTOR_BASE_DIR=example/demo-role/ \
    -e ANSIBLE_DOCTOR_RENDERER__FORCE_OVERWRITE=true \
    -e ANSIBLE_DOCTOR_RENDERER__INCLUDE_HEADER=HEADER.md \
    -e ANSIBLE_DOCTOR_LOGGING__LEVEL=info \
    -e PY_COLORS=1 \
    -v $(pwd):/doctor \
    -w /doctor \
    thegeeklab/ansible-doctor
```

All environment configuration options are listed on the [environment variables](https://ansible-doctor.geekdocs.de/usage/configuration/#environment-variables) section.

{{< hint type=note >}}
Keep in mind, that SELinux labels (`:Z` or `:z`) need to be passed as mount option on SELinux enabled systems.
{{< /hint >}}
