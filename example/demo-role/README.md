# demo-role-custom-header

[![Build Status](https://img.shields.io/drone/build/thegeeklab/ansible-doctor?logo=drone&server=https%3A%2F%2Fdrone.thegeeklab.de)](https://drone.thegeeklab.de/thegeeklab/ansible-doctor)
[![License: GPL-3.0](https://img.shields.io/github/license/thegeeklab/ansible-doctor)](https://github.com/thegeeklab/ansible-doctor/blob/main/LICENSE)

Role to demonstrate ansible-doctor. It is also possible to overwrite
the default description with an annotation.

## Table of content

- [Requirements](#requirements)
- [Default Variables](#default-variables)
  - [demo_role_deprecated](#demo_role_deprecated)
  - [demo_role_deprecated_info](#demo_role_deprecated_info)
  - [demo_role_dict](#demo_role_dict)
  - [demo_role_empty](#demo_role_empty)
  - [demo_role_empty_dict](#demo_role_empty_dict)
  - [demo_role_other_tags](#demo_role_other_tags)
  - [demo_role_override](#demo_role_override)
  - [demo_role_override_complex](#demo_role_override_complex)
  - [demo_role_single](#demo_role_single)
  - [demo_role_undefined_var](#demo_role_undefined_var)
  - [demo_role_unset](#demo_role_unset)
- [Discovered Tags](#discovered-tags)
- [Open Tasks](#open-tasks)
- [Dependencies](#dependencies)
- [License](#license)
- [Author](#author)

---

## Requirements

- Minimum Ansible version: `2.10`

## Default Variables

### demo_role_deprecated

**_Deprecated_**<br />

#### Default value

```YAML
demo_role_deprecated: b
```

### demo_role_deprecated_info

**_Deprecated:_** This variable is deprected since `v2.0.0` and will be removed in a future release.<br />
**_Type:_** string<br />

#### Default value

```YAML
demo_role_deprecated_info: a
```

### demo_role_dict

#### Default value

```YAML
demo_role_dict:
  key1:
    sub: some value
```

#### Example usage

```YAML
demo_role_dict:
  key1:
    sub: some value

  # Inline description
  key2:
    sublist:
      - subval1
      - subval2
```

### demo_role_empty

#### Default value

```YAML
demo_role_empty: ''
```

### demo_role_empty_dict

... or valid json can be used. In this case, the json will be automatically prefixed with the annotation key
and filters like `to_nice_yaml` can be used in templates. To get it working, the json need to be prefixed with a `$`.

#### Default value

```YAML
demo_role_empty_dict: {}
```

#### Example usage

```YAML
demo_role_empty_dict:
  key1:
    sub: some value
  key2:
    sublist:
      - subval1
      - subval2
```

### demo_role_other_tags

If a variable need some more explanation, this is a good place to do so.

#### Default value

```YAML
demo_role_other_tags: []
```

#### Example usage

```YAML
demo_role_other_tags:
  - package1
  - package2
```

### demo_role_override

#### Default value

```YAML
demo_role_override: test
```

### demo_role_override_complex

#### Default value

```YAML
demo_role_override_complex:
  foo: bar
  second: value
```

### demo_role_single

#### Default value

```YAML
demo_role_single: b
```

### demo_role_undefined_var

To highlight a variable that has not set a value by default, this is one way to achieve it.
Make sure to flag it as json value: `@var demo_role_undefined_var: $ "_unset_"`

| Attribute | Description |
| --- | --- |
| value1 | desc1 |

#### Default value

```YAML
demo_role_undefined_var: _unset_
```

### demo_role_unset

Values can be plain strings, but there is no magic or autoformatting...

#### Default value

```YAML
demo_role_unset:
```

#### Example usage

```YAML
demo_role_unset: some_value
```

## Discovered Tags

**_role-tag1_**

**_role-tag2_**

**_single-tag_**\
&emsp;Example description of tag `single-tag`

## Open Tasks

- Unscoped general todo.
- (bug): Some bug that is known and need to be fixed.
- (bug): Multi line description are possible as well. Some bug that is known and need to be fixed.
- (improvement): Some things that need to be improved.

## Dependencies

- role1
- role2

## License

MIT

## Author

[John Doe](https://blog.example.com)
