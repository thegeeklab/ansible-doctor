# other-role-custom-header

[![Build Status](https://ci.thegeeklab.de/api/badges/thegeeklab/ansible-doctor/status.svg)](https://ci.thegeeklab.de/repos/thegeeklab/ansible-doctor)
[![License: GPL-3.0](https://img.shields.io/github/license/thegeeklab/ansible-doctor)](https://github.com/thegeeklab/ansible-doctor/blob/main/LICENSE)

Role to demonstrate ansible-doctor.

## Table of contents

- [Requirements](#requirements)
- [Default Variables](#default-variables)
  - [other_role_bool](#other_role_bool)
  - [other_role_deprecated](#other_role_deprecated)
  - [other_role_deprecated_info](#other_role_deprecated_info)
  - [other_role_dict](#other_role_dict)
  - [other_role_empty](#other_role_empty)
  - [other_role_empty_dict](#other_role_empty_dict)
  - [other_role_multiline_type](#other_role_multiline_type)
  - [other_role_other_tags](#other_role_other_tags)
  - [other_role_override](#other_role_override)
  - [other_role_override_complex](#other_role_override_complex)
  - [other_role_single](#other_role_single)
  - [other_role_undefined_var](#other_role_undefined_var)
  - [other_role_unset](#other_role_unset)
- [Discovered Tags](#discovered-tags)
- [Open Tasks](#open-tasks)
- [Dependencies](#dependencies)
- [License](#license)
- [Author](#author)

---

## Requirements

- Minimum Ansible version: `2.10`

## Default Variables

### other_role_bool

#### Default value

```YAML
other_role_bool: true
```

#### Example usage

```YAML
other_role_bool: false
```

### other_role_deprecated

**_Deprecated_**<br />

#### Default value

```YAML
other_role_deprecated: b
```

### other_role_deprecated_info

**_Deprecated:_** This variable is deprecated since `v2.0.0` and will be removed in a future release.<br />
**_Type:_** string<br />

#### Default value

```YAML
other_role_deprecated_info: a
```

### other_role_dict

#### Default value

```YAML
other_role_dict:
  key1:
    sub: some value
```

#### Example usage

```YAML
other_role_dict:
  key1:
    sub: some value

  # Inline description
  key2:
    sub_list:
      - sub_val1
      - sub_val2
```

### other_role_empty

#### Default value

```YAML
other_role_empty: ''
```

### other_role_empty_dict

... or valid json can be used. In this case, the json will be automatically prefixed with the annotation key
and filters like `to_nice_yaml` can be used in templates. To get it working, the json need to be prefixed with a `$`.

#### Default value

```YAML
other_role_empty_dict: {}
```

#### Example usage

```YAML
other_role_empty_dict:
  key1:
    sub: some value
  key2:
    sub_list:
      - sub_val1
      - sub_val2
```

### other_role_multiline_type

**_Type:_** string
list
dict<br />

#### Default value

```YAML
other_role_multiline_type: a
```

### other_role_other_tags

If a variable need some more explanation, this is a good place to do so.

#### Default value

```YAML
other_role_other_tags:
  - package1
  - package2
```

#### Example usage

```YAML
other_role_other_tags:
  - package1
  - package2
```

### other_role_override

#### Default value

```YAML
other_role_override: test
```

### other_role_override_complex

#### Default value

```YAML
other_role_override_complex:
  foo: bar
  second: value
```

### other_role_single

#### Default value

```YAML
other_role_single: b
```

### other_role_undefined_var

To highlight a variable that has not set a value by default, this is one way to achieve it.
Make sure to flag it as json value: `@var other_role_undefined_var: $ "_unset_"`

| Attribute | Description |
| --- | --- |
| value1 | desc1 |

#### Default value

```YAML
other_role_undefined_var: _unset_
```

### other_role_unset

Values can be plain strings, but there is no magic or autoformatting...

#### Default value

```YAML
other_role_unset:
```

#### Example usage

```YAML
other_role_unset: some_value
```

## Discovered Tags

**_role-tag1_**

**_role-tag2_**

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
