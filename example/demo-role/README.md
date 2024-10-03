# demo-role-custom-header

[![Build Status](https://ci.thegeeklab.de/api/badges/thegeeklab/ansible-doctor/status.svg)](https://ci.thegeeklab.de/repos/thegeeklab/ansible-doctor)
[![License: GPL-3.0](https://img.shields.io/github/license/thegeeklab/ansible-doctor)](https://github.com/thegeeklab/ansible-doctor/blob/main/LICENSE)

Role to demonstrate ansible-doctor. It is also possible to overwrite
the default description with an annotation.

## Table of content

- [Requirements](#requirements)
- [Default Variables](#default-variables)
- [Discovered Tags](#discovered-tags)
- [Open Tasks](#open-tasks)
- [Dependencies](#dependencies)
- [License](#license)
- [Author](#author)

---

## Requirements

- Minimum Ansible version: `2.10`

## Default Variables

|Variable|Default|Description|Type|Deprecated|Example|
|--------|-------|-----------|----|----------|-------|
|demo_bool|True|||False|demo_bool|
|demo_role_deprecated|b|||True||
|demo_role_deprecated_info|a||string|This variable is deprected since `v2.0.0` and will be removed in a future release.||
|demo_role_dict|{'key1': {'sub': 'some value'}}|||False|demo_role_dict:<br /> key1:<br /> sub: some value<br /><br /><br /># Inline description<br /> key2:<br /> sublist:<br /> - subval1<br /> - subval2|
|demo_role_empty||||False||
|demo_role_empty_dict|{}|... or valid json can be used. In this case, the json will be automatically prefixed with the annotation key<br />and filters like `to_nice_yaml` can be used in templates. To get it working, the json need to be prefixed with a `$`.||False|demo_role_empty_dict|
|demo_role_other_tags|[]|If a variable need some more explanation, this is a good place to do so.||False|demo_role_other_tags|
|demo_role_override|test|||False||
|demo_role_override_complex|{'foo': 'bar', 'second': 'value'}|||False||
|demo_role_single|b|||False||
|demo_role_undefined_var|_unset_|To highlight a variable that has not set a value by default, this is one way to achieve it.<br />Make sure to flag it as json value: `@var demo_role_undefined_var: $ "_unset_"`<br /><br /><br />\| Attribute \| Description \|<br />\| --- \| --- \|<br />\| value1 \| desc1 \|||False||
|demo_role_unset|None|Values can be plain strings, but there is no magic or autoformatting...||False|demo_role_unset: some_value|

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

- role2

## License

MIT

## Author

[John Doe](https://blog.example.com)
