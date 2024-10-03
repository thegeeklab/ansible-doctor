# other-role-custom-header

[![Build Status](https://ci.thegeeklab.de/api/badges/thegeeklab/ansible-doctor/status.svg)](https://ci.thegeeklab.de/repos/thegeeklab/ansible-doctor)
[![License: GPL-3.0](https://img.shields.io/github/license/thegeeklab/ansible-doctor)](https://github.com/thegeeklab/ansible-doctor/blob/main/LICENSE)

Role to demonstrate ansible-doctor.

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
|`demo_bool`|`True`|||False|`{'demo_bool': False}`|
|`other_role_deprecated`|`b`|||True||
|`other_role_deprecated_info`|`a`||`string`|This variable is deprected since `v2.0.0` and will be removed in a future release.||
|`other_role_dict`|`{'key1': {'sub': 'some value'}}`|||False|other_role_dict:<br /> key1:<br /> sub: some value<br /><br /><br /># Inline description<br /> key2:<br /> sublist:<br /> - subval1<br /> - subval2|
|`other_role_empty`||||False||
|`other_role_empty_dict`||... or valid json can be used. In this case, the json will be automatically prefixed with the annotation key<br />and filters like `to_nice_yaml` can be used in templates. To get it working, the json need to be prefixed with a `$`.||False|`{'other_role_empty_dict': {'key1': {'sub': 'some value'}, 'key2': {'sublist': ['subval1', 'subval2']}}}`|
|`other_role_multiline_type`|`a`||string<br />list<br />dict|False||
|`other_role_other_tags`||If a variable need some more explanation, this is a good place to do so.||False|`{'other_role_other_tags': ['package1', 'package2']}`|
|`other_role_override`|`test`|||False||
|`other_role_override_complex`|`{'foo': 'bar', 'second': 'value'}`|||False||
|`other_role_single`|`b`|||False||
|`other_role_undefined_var`|`_unset_`|To highlight a variable that has not set a value by default, this is one way to achieve it.<br />Make sure to flag it as json value: `@var other_role_undefined_var: $ "_unset_"`<br /><br /><br />\| Attribute \| Description \|<br />\| --- \| --- \|<br />\| value1 \| desc1 \|||False||
|`other_role_unset`||Values can be plain strings, but there is no magic or autoformatting...||False|`other_role_unset: some_value`|

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
