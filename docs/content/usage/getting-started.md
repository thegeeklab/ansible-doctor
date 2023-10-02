---
title: Getting Started
---

{{< toc >}}

## Getting Started

```Shell
ansible-doctor FOLDER
```

If no folder is passed to _ansible-doctor_, the current working directory is used. The first step is to determine if the specified folder is an Ansible role. This check is very simple and only verifies if there is a sub-directory named `tasks` in the specified folder. After a successful check, _ansible-doctor_ registers all files of the role to search them for annotations.

Without any further work _ansible-doctor_ can already create a documentation of the available variables and some meta information if the role contains. This basic information can be extended with a set of available annotations. If you want to see it in action you can find a [demo role](https://github.com/thegeeklab/ansible-doctor/tree/main/example) with a lot of examples in the repository.

## Annotations

In general, an annotation is a comment with an identifier followed by colon separated options and a value. A [complex example](https://github.com/thegeeklab/ansible-doctor/tree/main/example) is available on the GitHub repository.

### `@meta`

Identifier to add role metadata information. The general structure for this identifier is `# @identifier option1: <value>`.

option1
: scope that can be chosen freely, but the built-in template only handles a few scopes `["dependencies", "license", "author"]`

**Example:**

```YAML
# @meta description: >
# Role to demonstrate ansible-doctor. It is also possible to overwrite
# the default description with an annotation.
# @end

# @meta author:value: [John Doe](https://blog.example.com)
```

### `@var`

Identifier to add extra documentation to Ansible variables. The general structure for this identifier is `# @identifier option1:option2: <value>`.

option1
: the name of the variable to which additional information should be added

option2
: supports `["value", "example", "description", "type", "deprecated"]` as information scopes

#### `value`

```yaml
# @var docker_registry_password:value: $ "secret"
docker_registry_password: "secret"
```

#### `example`

```yaml
# @var docker_registry_password:example: $ "randomPassw0rd"
# @var docker_registry_password:example: >
# docker_registry_password: "randomPassw0rd"
# @end
docker_registry_password: "secret"
```

#### `description`

```yaml
# @var docker_registry_password:description: Very secure password to login to the docker registry.
# @var docker_registry_password:description: >
# Multi line description are possible as well.
# Very secure password to login to the docker registry.
# @end
docker_registry_password: "secret"
```

#### `type`

```yaml
# @var docker_registry_password:type: string
docker_registry_password: "secret"
```

#### `deprecated`

```yaml
# @var docker_registry_password:deprecated: true
# @var docker_registry_password:deprecated: since v1.0.0
docker_registry_password: "secret"
```

### `@tag`

Used tags within the Ansible task files will be auto-discovered. This identifier can be used to define tags manually or add extended information to discovered tags.

option1
: the name of the tag to which additional information should be added

option2
: supports `["value", "description"]` as information scopes

**Example:**

```YAML
- name: Demo task with a tag list
  debug:
    msg: "Demo message"
  tags:
    - role-tag1
    - role-tag2

# @tag single-tag:description: Example description of tag `single-tag`
- name: Demo task with a single tag
  debug:
    msg: "Demo message"
  tags: single-tag
```

### `@todo`

Identifier to open tasks that need to be addressed. The general structure for this identifier is `# @identifier option1: <value>`.

option1
: scope that can be chosen freely, e.g. `bug`, `improvement`

**Example:**

```YAML
# @todo bug: Some bug that is known and need to be fixed.
# @todo bug: >
# Multi line description are possible as well.
# Some bug that is known and need to be fixed.
# @end

# @todo improvement: Some things that need to be improved.

# @todo default: Unscoped general todo.
```
