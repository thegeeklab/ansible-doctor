---
title: Usage
---

```Shell
ansible-doctor FOLDER
```

If you don't pass a folder to *ansible-doctor* your current working directory will be used. The first step is to identify if the given folder is an ansible role. This check is very simple, if the folder contains a subfolder called `tasks` is MUST be an ansible role! :)

After the successful check, *ansible-doctor* will try to read some static files into a dictionary:

* defaults/main.yml
* meta/main.yml

This will be the base result set which is used as data source for every output template. Without any work, you will get at least a documentation about available variables and some meta information. Theses basic information can be expanded with a set of available annotations. In general, an annotation is a comment with an identifier. This identifier is followed by colon separated options and ends with a value.

{{< highlight Yaml "linenos=table" >}}
# @identifier option1:option2: <value>

# @var docker_registry_password:example: "%8gv_5GA?"
# @var docker_registry_password:description: Very secure password to login to the docker registry
# @var docker_registry_password:description: >
# You can also write it as multiline description
# Very secure password to login to the docker registry.
# @end
docker_registry_password: "secret"
{{< /highlight >}}

These list of pre-defined identifiers is currently available:

* @meta
* @todo
* @var
* @tag
