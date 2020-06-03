---
title: Default settings
---

<!-- markdownlint-disable -->
{{< highlight YAML "linenos=table" >}}
---
# default is your current working dir
role_dir:
# default is the basename of 'role_name'
role_name:
# don't write anything to file system
dry_run: False

logging:
    # possible options debug | info | warning | error | critical
    level: "warning"
    # you can enable json logging if a parsable output is required
    json: False

# path to write rendered template file
# default is your current working dir
output_dir:
# default is in-build templates dir
template_dir:
template: readme

# don't ask to overwrite if output file exists
force_overwrite: False
# load custom header from given file and append template output
# to it before write.
custom_header: ""

exclude_files: []
# Examples
# exclude_files:
#   - molecule/
#   - files/**/*.py
{{< /highlight >}}
<!-- markdownlint-restore -->
