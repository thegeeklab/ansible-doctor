# demo-role-custom-header

[![Build Status](https://cloud.drone.io/api/badges/thegeeklab/ansible-doctor/status.svg)](https://cloud.drone.io/thegeeklab/ansible-doctor)
![License](https://img.shields.io/github/license/thegeeklab/ansible-doctor)

Role to demonstrate ansible-doctor. It is also possible to overwrite the default description with an annotation.

## Table of content

* [Default Variables](#default-variables)
  * [demo_role_unset](#demo_role_unset)
  * [demo_role_empty](#demo_role_empty)
  * [demo_role_single](#demo_role_single)
  * [demo_role_empty_dict](#demo_role_empty_dict)
  * [demo_role_dict](#demo_role_dict)
  * [demo_role_other_tags](#demo_role_other_tags)
  * [demo_role_undefined_var](#demo_role_undefined_var)
* [Dependencies](#dependencies)
* [License](#license)
* [Author](#author)

---

## Default Variables

### demo_role_unset

You can set values as string, but there is no magic or autoformatting...

#### Default value

```YAML
demo_role_unset:
```

#### Example usage

```YAML
demo_role_unset: some_value
```

### demo_role_empty

#### Default value

```YAML
demo_role_empty: ''
```

### demo_role_single

#### Default value

```YAML
demo_role_single: b
```

### demo_role_empty_dict

... or you can use a valid json. In this case, the json will be automatically prefixed with the annotation key and you can use e.g. `to_nice_yaml` filter in your templates. To get this working, you have to prefix your json with a `$` char.

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

### demo_role_undefined_var

If you want to add an explicit notice, that a var is not set by default, this is one option. Make sure to flag it as json value: `@var demo_role_undefined_var: $ "_unset_"`

#### Default value

```YAML
demo_role_undefined_var: _unset_
```

## Dependencies

None.

## License

MIT

## Author

Robert Kaussow <mail@example.com>
