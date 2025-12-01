---
title: Templates
---

## Overview

Ansible Doctor uses a template system to generate documentation from Ansible roles. Templates are written in Jinja2 and can be customized to fit different documentation formats and styles.

## Available Templates

Ansible Doctor comes with several built-in templates:

### readme

- **Location**: `ansibledoctor/templates/readme/README.md.j2`
- **Format**: Markdown
- **Description**: Generates a standard README.md

### readme-adoc

- **Location**: `ansibledoctor/templates/readme-adoc/README.adoc.j2`
- **Format**: AsciiDoc
- **Description**: Generates an AsciiDoc document for AsciiDoc processors

#### Customization

These AsciiDoc templates adhere as closely as possible to the original Markdown templates, primarily replacing Markdown syntax with AsciiDoc syntax, with **one notable exception**: Table of Contents (TOC) generation.

Ansible-doctor's Markdown templates hardcode a TOC into the template, making it visible in the generated Markdown TXT file. I decided not to hardcode the TOC into the TXT file, as I see the benefit of a TOC only in non-TXT output formats like HTML or PDF, which allow navigation using a mouse.

For this reason, the AsciiDoc templates do not hardcode a TOC into the template. Instead, they use the built-in `:toc:` and `:toclevels: 2` attributes. The AsciiDoc output file will not contain a TOC, but converters will automatically generate a 2-level deep TOC when producing HTML, PDF, or other output formats from the AsciiDoc file.

The default settings for automatic TOC generation are placed in `README.adoc.j2` directly after the title line:

```jinja
{% if not append | deep_get(role, "internal.append") %}
{% set meta = role.meta | default({}) %}
= {{ meta.name.value | safe_join(" ") }}
\:toc:                                                          <!-- 1 -->
\:toclevels: 2                                                  <!-- 2 -->
{% endif %}
{% if description | deep_get(meta, "description.value") %}
```

1. `:toc:` enables TOC generation.
2. `:toclevels: 2` limits the TOC to 2 levels, matching the hardcoded TOC in the Markdown template.

---

To override these defaults (e.g., in a `HEADER.adoc` file), create custom settings for `ansible-doctor` in a `.ansibledoctor.yml` file and configure it to use your `HEADER.adoc` in the `renderer` section:

```yaml
renderer:
  include_header: HEADER.adoc
```

Then, create the `HEADER.adoc` file in the top directory of your role and adjust `:toc:`, `:toclevels:`, or disable TOC generation with `:!toc:`. You can also add other attributes in the document header section:

```adoc
= demo-role-custom-header
\:subject: demo-role-custom-header
\:description: Lorem ipsum dolor nisi sunt...
\:keywords: ansible-doctor template asciidoc
\:author: Patrick Ben Koetter
\:email: p@sys4.de
\:source-highlighter: rouge
\:rouge-style: base16
\:toc:
\:toclevels: 2
\:revnumber: 0.1
\:revdate: 09.11.2025
\:status: draft
\:publisher: sys4 AG
\:copyright: (C) sys4 AG
\:lang: de
\:hyphens: de
\:encoding: UTF-8
\:pdf-version: 1.7
\:sectnums:
\:pagenums:
\:sectanchors:
\:icons: image
\:iconsdir: ./corporatedesign/icons
\:title-page:
\:pdf-theme: ./corporatedesign/sys4.yml
\:pdf-fontsdir: ./corporatedesign/fonts/
\:stylesheet: ./corporatedesign/css/standalone.css
```

### hugo-book

- **Location**: `ansibledoctor/templates/hugo-book/index.md.j2`
- **Format**: Markdown with Hugo front matter
- **Description**: Generates documentation compatible with Hugo themes

## Using Templates

To use templates with Ansible Doctor:

1. **Default usage**: Simply run `ansible-doctor` in your role directory to use the default README template.

2. **Custom template**: Specify a custom template in your configuration:

   ```yaml
   template:
     name: readme
     src: local>/path/to/custom/templates/
   ```

3. **Git-based template**: Use a template from a Git repository:

   ```yaml
   template:
     name: readme
     src: git>https://github.com/username/repo
   ```

4. **Template options**: Configure template rendering options:

   ```yaml
   template:
     options:
       tabulate_vars: true # Display variables in table format
       sort_vars: true # Sort variables alphabetically
   ```

## Creating Custom Templates

To create your own templates:

1. Create a directory structure similar to the built-in templates
2. Implement your main template file (e.g., `README.md.j2`)
3. Create any partial templates you need
4. Use the standard template variables and helpers provided by Ansible Doctor

Refer to the existing templates in `ansibledoctor/templates/` for examples of how to structure your custom templates.
