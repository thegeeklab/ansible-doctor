---
title: Configuration
---

_ansible-doctor_ comes with default settings which should be sufficient for most users to start, but you can adjust most settings to your needs.

Changes can be made on different locations which will be processed in the following order (last wins):

- default configuration (build-in)
- global configuration file (path depends on your operating system)
- folder-based configuration file (.ansibledoctor.yml|.ansibledoctor.yaml|.ansibledoctor in current working directory)
- environment variables
- CLI options
