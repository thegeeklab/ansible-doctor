---
title: Templates
# cspell:ignore adoc revdate revnumber toclevels
---

Ansible Doctor employs a flexible template system to generate documentation from Ansible roles. Built on Jinja2, these templates can be customized to produce documentation in various formats and styles.

## Built-in Templates

Ansible Doctor includes several pre-built templates:

### README (`readme`)

- **Location**: `ansibledoctor/templates/readme/README.md.j2`
- **Format**: Markdown
- **Description**: Generates a standard README.md file

### AsciiDoc (`readme-adoc`)

- **Location**: `ansibledoctor/templates/readme-adoc/README.adoc.j2`
- **Format**: AsciiDoc
- **Description**: Generates AsciiDoc documentation for AsciiDoc processors

#### Customization

The AsciiDoc templates maintain consistency with their Markdown counterparts while leveraging AsciiDoc's native features. One key difference is in Table of Contents (TOC) handling:

- **Markdown approach**: Hardcoded TOC in the template
- **AsciiDoc approach**: Uses native `:toc:` and `:toclevels: 2` attributes

This approach keeps the AsciiDoc source clean while enabling automatic TOC generation in output formats like HTML and PDF.

Default TOC configuration in `README.adoc.j2`:

```jinja
{% if not append | deep_get(role, "internal.append") %}
{% set meta = role.meta | default({}) %}
= {{ meta.name.value | safe_join(" ") }}
:toc:                                                          <!-- 1 -->
:toclevels: 2                                                  <!-- 2 -->
{% endif %}
{% if description | deep_get(meta, "description.value") %}
```

1. `:toc:` enables automatic TOC generation
2. `:toclevels: 2` limits TOC to 2 levels

To customize these settings, create a `.ansibledoctor.yml` configuration:

```yaml
renderer:
  include_header: HEADER.adoc
```

Then create a `HEADER.adoc` file with your preferred attributes:

```adoc
= demo-role-custom-header
:subject: demo-role-custom-header
:description: Lorem ipsum dolor nisi...
:keywords: ansible-doctor template asciidoc
:author: Patrick Ben Koetter
:email: p@sys4.de
:source-highlighter: rouge
:rouge-style: base16
:toc:
:toclevels: 2
:revnumber: 0.1
:revdate: 09.11.2025
:status: draft
:publisher: sys4 AG
:copyright: (C) sys4 AG
:lang: de
:hyphens: de
:encoding: UTF-8
:pdf-version: 1.7
```

You can read more about document attributes in [AsciiDoc's documentation](https://docs.asciidoctor.org/asciidoc/latest/attributes/document-attributes/).

### Hugo Book (`hugo-book`)

- **Location**: `ansibledoctor/templates/hugo-book/index.md.j2`
- **Format**: Markdown with Hugo front matter
- **Description**: Generates documentation compatible with Hugo themes

## Usage

Run `ansible-doctor` in your role directory to use the default README template.

### Custom Template Configuration

Specify a custom template in your `.ansibledoctor.yml`:

```yaml
template:
  name: readme
  src: local>/path/to/custom/templates/
```

### Git-based Templates

Use templates from a Git repository:

```yaml
template:
  name: readme
  src: git>https://github.com/username/repo
```

### Template Rendering Options

Configure how templates are rendered:

```yaml
template:
  options:
    tabulate_vars: true # Display variables in table format
    sort_vars: true # Sort variables alphabetically
```

## Creating Custom Templates

1. **Directory Structure**: Create a structure similar to the built-in templates
2. **Main Template**: Implement your primary template file (e.g., `README.md.j2`)
3. **Partial Templates**: Create reusable template components as needed
4. **Standard Features**: Utilize Ansible Doctor's template variables and helpers

For examples, examine the existing templates in `ansibledoctor/templates/`.
