
ansible role for Amazon's Java implementation corretto.


[![GitHub Workflow Status](https://img.shields.io/github/workflow/status/bodsch/ansible-corretto-java/CI)][ci]
[![GitHub issues](https://img.shields.io/github/issues/bodsch/ansible-corretto-java)][issues]
[![GitHub release (latest by date)](https://img.shields.io/github/v/release/bodsch/ansible-corretto-java)][releases]

[ci]: https://github.com/bodsch/ansible-corretto-java/actions
[issues]: https://github.com/bodsch/ansible-corretto-java/issues?q=is%3Aopen+is%3Aissue
[releases]: https://github.com/bodsch/ansible-corretto-java/releases

default java version is 11

## tested operating systems

- CentOS 7 / 8
- Ubuntu 16 / 18
- Debian 9 / 10

## Supported Versions

- [corretto-8](https://docs.aws.amazon.com/corretto/latest/corretto-8-ug)
- [corretto-11](https://docs.aws.amazon.com/corretto/latest/corretto-11-ug)
- [corretto-15](https://docs.aws.amazon.com/corretto/latest/corretto-15-ug)


# downloads


## configuration parameters

```
java_version: 11

java_folder: /usr/lib/jvm
java_alias: "java-{{ java_version }}-corretto"

java_map:
  redhat:
    8: { url: "https://corretto.aws/downloads/resources/8.242.08.1/java-1.8.0-amazon-corretto-devel-1.8.0_242.b08-1.x86_64.rpm", checksum: "md5:af146bc202ca2651381b286364ef45e2" }
    11: { url: "https://corretto.aws/downloads/resources/11.0.6.10.1/java-11-amazon-corretto-devel-11.0.6.10-1.x86_64.rpm", checksum: "md5:1e08469d0fbf8bd737171e4590721b1f" }

  debian:
    8: { url: "https://corretto.aws/downloads/resources/8.242.08.1/java-1.8.0-amazon-corretto-jdk_8.242.08-1_amd64.deb", checksum: "md5:3ece5f8ab9d68917e541e14c1fee6909" }
    11: { url: "https://corretto.aws/downloads/resources/11.0.6.10.1/java-11-amazon-corretto-jdk_11.0.6.10-1_amd64.deb", checksum: "md5:501e257d5389e26a024c01b47b4a8d80" }

  src:
    8: { url: "https://corretto.aws/downloads/resources/8.242.08.1/amazon-corretto-8.242.08.1-linux-x64.tar.gz", checksum: "md5:3a614a0e32aa5324843781d1077aad7a" }
    11: { url: "https://corretto.aws/downloads/resources/11.0.6.10.1/amazon-corretto-11.0.6.10.1-linux-x64.tar.gz", checksum: "md5:cfb0b142edf7ebc2f87a27405c8d39fc" }
```
