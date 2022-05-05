
# Ansible Role:  `java`

Ansible role to install different Java versions.  
During installation, mak can choose between *JDK* and *JRE* (When the required archive is available!).


[![GitHub Workflow Status](https://img.shields.io/github/workflow/status/bodsch/ansible-java/CI)][ci]
[![GitHub issues](https://img.shields.io/github/issues/bodsch/ansible-java)][issues]
[![GitHub release (latest by date)](https://img.shields.io/github/v/release/bodsch/ansible-java)][releases]

[ci]: https://github.com/bodsch/ansible-java/actions
[issues]: https://github.com/bodsch/ansible-java/issues?q=is%3Aopen+is%3Aissue
[releases]: https://github.com/bodsch/ansible-java/releases


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

java_type: "jre"

java_version_map:
  "8": "OpenJDK8U-jdk_x64_linux_hotspot_8u275b01.tar.gz"
  "9": "OpenJDK9U-jdk_x64_linux_hotspot_9.0.4_11.tar.gz"
  "10": "OpenJDK10U-jdk_x64_linux_hotspot_10.0.2_13.tar.gz"
  "11": "OpenJDK11U-{{ java_type }}_x64_linux_{{ java_jvm }}_11.0.15_10.tar.gz"
  "12": "OpenJDK12U-{{ java_type }}_x64_linux_{{ java_jvm }}_12.0.2_10.tar.gz"
  "13": "OpenJDK13U-{{ java_type }}_x64_linux_{{ java_jvm }}_13.0.2_8.tar.gz"
  "14": "OpenJDK14U-{{ java_type }}_x64_linux_{{ java_jvm }}_14.0.2_12.tar.gz"
  "15": "OpenJDK15U-{{ java_type }}_x64_linux_{{ java_jvm }}_15.0.2_7.tar.gz"
  "16": "OpenJDK16U-{{ java_type }}_x64_linux_{{ java_jvm }}_16.0.2_7.tar.gz"


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
  "11": "OpenJDK11U-jdk_x64_linux_hotspot_11.0.10.2_1.tar.gz"
  "12": "OpenJDK12U-jdk_x64_linux_hotspot_12.0.5_11.tar.gz"
```

Below the directory `java_install_directory` a new directory is created for each Java version.

This makes it possible to store several versions of a JDK and to activate them selectively.

In each of the directories a `profile.sh` file is created which exports the `JAVA_HOME`,
and extends the `PATH` variables.

**There is no Java version activated by default!**


#### Example

| Filename | Major Version | Full Version | Installation path | Comments |
| :-----     | :-----        | :-----       | :-----         | :--- |
| `OpenJDK8U-jdk_x64_linux_hotspot_8u275b01.tar.gz`   | `8`  | `8u275b01` | `/opt/java/jdk-8u275b01` | old versioning. **OBSOLETE** |
| `OpenJDK10U-jdk_x64_linux_hotspot_10.0.2_13.tar.gz` | `10` | `10.0.2`   | `/opt/java/jdk-10.0.2`   | |
| `OpenJDK15U-jdk_x64_linux_hotspot_15.0.1_9.tar.gz`  | `15` | `15.0.1`   | `/opt/java/jdk-15.0.1`   | |
| `OpenJDK16-jdk_x64_linux_hotspot_16_36.tar.gz`      | `16` | `16`       | `/opt/java/jdk-16`       | **PRE RELEASE** |
| `OpenJDK16U-jdk_x64_linux_hotspot_16.0.1_9.tar.gz`  | `16` | `16.0.1`   | `/opt/java/jdk-16.0.1`   | |


---

## Author

- Bodo Schulz

## License

[Apache](LICENSE)

`FREE SOFTWARE, HELL YEAH!`
