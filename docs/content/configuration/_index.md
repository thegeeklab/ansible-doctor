---
title: Configuration
---

*ansible-doctor* comes with default settings which should be sufficient for most users to start, but you can adjust most settings to your needs.

Changes can be made on different locations which will be processed in the following order (last wins):

* default config (build-in)
* global config file (path depends on your operating system)
* folder-based config file (.ansibledoctor.yml|.ansibledoctor.yaml|.ansibledoctor in current working dir)
* environment variables
* cli options
