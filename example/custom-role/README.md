# custom-role

Example role demonstrating custom sections via local template include.

## Table of contents

- [Requirements](#requirements)
- [Default Variables](#default-variables)
  - [custom_role_greeting](#custom_role_greeting)
- [Dependencies](#dependencies)
- [License](#license)
- [Author](#author)

---

## Requirements

This `_requirements.j2` lives in `.ansibledoctor/` inside the role directory and
overrides the template default. It is picked up because `.ansibledoctor/`
takes precedence in the Jinja2 search path.

- Minimum Ansible version: `2.10`

## Custom Information

This section is included from `.ansibledoctor/CUSTOM_SECTION.md`. The
overridden `_requirements.j2` includes it with a Jinja2 include statement that
has ignore missing enabled. Delete this file and the section disappears
without breaking the build.

## Default Variables

### custom_role_greeting

A greeting message rendered by the role.

**_Type:_** string<br />

#### Default value

```YAML
custom_role_greeting: Hello from custom-role
```

#### Example usage

```YAML
"Hello world"
```

## Dependencies

None.

## License

MIT

## Author

ansible-doctor
