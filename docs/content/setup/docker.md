---
title: Using docker

---

{{< highlight Shell "linenos=table" >}}
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
{{< /highlight >}}

{{< hint info >}}
**Info**\
Keep in mind, that you have to pass SELinux labels (:Z or :z) to your mount option if you are working on SELinux enabled systems.
{{< /hint >}}
