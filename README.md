
# Ansible Role:  `java`

Ansible role to install different Java versions.  
During installation, mak can choose between *JDK* and *JRE* (When the required archive is available!).


[![GitHub Workflow Status](https://img.shields.io/github/workflow/status/bodsch/ansible-java/CI)][ci]
[![GitHub issues](https://img.shields.io/github/issues/bodsch/ansible-java)][issues]
[![GitHub release (latest by date)](https://img.shields.io/github/v/release/bodsch/ansible-java)][releases]

[ci]: https://github.com/bodsch/ansible-java/actions
[issues]: https://github.com/bodsch/ansible-java/issues?q=is%3Aopen+is%3Aissue
[releases]: https://github.com/bodsch/ansible-java/releases


All archives are stored on the Ansible controller. These are then copied to the target system and unpacked into the target directory.

The cache directory can be defined via the environment variable `CUSTOM_LOCAL_TMP_DIRECTORY`. 
By default it is `${HOME}/.cache/ansible/java`.  
If this type of installation is not desired, the download can take place directly on the target system. 
However, this must be explicitly activated by setting `java_direct_download` to `true`.


## tested operating systems

* ArchLinux
* Debian based
    - Debian 10 / 11
    - Ubuntu 20.04

## Contribution

Please read [Contribution](CONTRIBUTING.md)

## Development,  Branches (Git Tags)

The `master` Branch is my *Working Horse* includes the "latest, hot shit" and can be complete broken!

If you want to use something stable, please use a [Tagged Version](https://gitlab.com/bodsch/ansible-java/-/tags)!

---

## usage

```yaml
java_automatic_cleanup: true

java_install_directory: /opt/java

java_versions: []

java_type: "jdk"

java_version_map:
  "11": "OpenJDK11U-jdk_x64_linux_hotspot_11.0.15_10.tar.gz"
  "12": "OpenJDK12U-jdk_x64_linux_hotspot_12.0.2_10.tar.gz"
  "13": "OpenJDK13U-jdk_x64_linux_hotspot_13.0.2_8.tar.gz"
  "14": "OpenJDK14U-jdk_x64_linux_hotspot_14.0.2_12.tar.gz"
  "15": "OpenJDK15U-jdk_x64_linux_hotspot_15.0.2_7.tar.gz"
  "16": "OpenJDK16U-jdk_x64_linux_hotspot_16.0.2_7.tar.gz"

java_default_version: ""
  
java_direct_download: false

java_download:
  url: https://github.com/adoptium
```

### Installation of different versions

The `java_version_map` can be used to control the real version.

`java_versions` is defined as a list and can also contain self-defined versions.

#### Example

```yaml
java_versions:
  - "11"
  - "12"

java_version_map:
  "11": "OpenJDK11U-jdk_x64_linux_hotspot_11.0.15_10.tar.gz"
  "12": "OpenJDK12U-jdk_x64_linux_hotspot_12.0.2_10.tar.gz"
```

Below the directory `java_install_directory` a new directory is created for each Java version.

This makes it possible to store several versions of a JDK and to activate them selectively.

In each of the directories a `profile.sh` file is created which exports the `JAVA_HOME`,
and extends the `PATH` variables.

**There is no Java version activated by default!**

But if you want to set a Java version as default, you can define `java_default_version` accordingly.


#### Example

| Filename | Major Version | Full Version | Installation path | Comments |
| :-----     | :-----        | :-----       | :-----         | :--- |
| `OpenJDK11U-jdk_x64_linux_hotspot_11.0.15_10.tar.gz` | `11` | `11.0.15`   | `/opt/java/jdk-11.0.15`   | |
| `OpenJDK16U-jdk_x64_linux_hotspot_16.0.2_7.tar.gz`   | `16` | `16.0.2`    | `/opt/java/jdk-16.0.2`    | |


---

## Author

- Bodo Schulz

## License

[Apache](LICENSE)

`FREE SOFTWARE, HELL YEAH!`
