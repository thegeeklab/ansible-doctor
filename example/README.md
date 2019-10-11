# demo-role-custom-header

[![Build Status](https://cloud.drone.io/api/badges/xoxys/ansible-doctor/status.svg)](https://cloud.drone.io/xoxys/ansible-doctor)
![License](https://img.shields.io/github/license/xoxys/ansible-doctor)

Role to demonstrate ansible-doctor

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

#### Default value

```YAML
demo_role_unset:
```

#### Example usage

```YAML
demo_role_unset: some value
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

Test oneline desc.

#### Default value

```YAML
  - _undefined_
```

## Dependencies

None.

## License

MIT

## Author

Robert Kaussow <mail@example.com>

