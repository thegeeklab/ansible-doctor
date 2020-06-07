---
title: CLI options
---

You can get all available CLI options by running `ansible-doctor --help`:

<!-- prettier-ignore-start -->
<!-- spellchecker-disable -->
{{< highlight Shell "linenos=table" >}}
$ ansible-doctor --help
usage: ansible-doctor [-h] [-c CONFIG_FILE] [-o OUTPUT_DIR] [-f] [-d] [-v]
                      [-q] [--version]
                      role_dir

Generate documentation from annotated Ansible roles using templates

positional arguments:
  role_dir              role directory (default: current working dir)

optional arguments:
  -h, --help            show this help message and exit
  -c CONFIG_FILE, --config CONFIG_FILE
                        location of configuration file
  -o OUTPUT_DIR, --output OUTPUT_DIR
                        output base dir
  -f, --force           force overwrite output file
  -d, --dry-run         dry run without writing
  -v                    increase log level
  -q                    decrease log level
  --version             show program's version number and exit
{{< /highlight >}}
<!-- spellchecker-enable -->
<!-- prettier-ignore-end -->
