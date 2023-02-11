# other-role-custom-header

[![Build Status](https://img.shields.io/drone/build/thegeeklab/ansible-doctor?logo=drone&server=https%3A%2F%2Fdrone.thegeeklab.de)](https://drone.thegeeklab.de/thegeeklab/ansible-doctor)
[![License: GPL-3.0](https://img.shields.io/github/license/thegeeklab/ansible-doctor)](https://github.com/thegeeklab/ansible-doctor/blob/main/LICENSE)

Role to demonstrate ansible-doctor. It is also possible to overwrite
the default description with an annotation.

## Table of content

- [Default Variables](#default-variables)
  - [demo_role_unset](#demo_role_unset)
- [Discovered Tags](#discovered-tags)
- [Open Tasks](#open-tasks)
- [Dependencies](#dependencies)
- [License](#license)
- [Author](#author)

---

## Default Variables

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
