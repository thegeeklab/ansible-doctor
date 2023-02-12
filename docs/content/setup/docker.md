---
title: Using docker
---

```Shell
docker run \
    -e ANSIBLE_DOCTOR_BASE_DIR=example/demo-role/ \
    -e ANSIBLE_DOCTOR_FORCE_OVERWRITE=true \
    -e ANSIBLE_DOCTOR_CUSTOM_HEADER=HEADER.md \
    -e ANSIBLE_DOCTOR_LOG_LEVEL=info \
    -e PY_COLORS=1 \
    -v $(pwd):/doctor \
    -w /doctor \
    thegeeklab/ansible-doctor
```

{{< hint type=note >}}
Keep in mind, that SELinux labels (`:Z` or `:z`) need to be passed as mount option on SELinux enabled systems.
{{< /hint >}}
