# python 3 headers, required if submitting to Ansible
from __future__ import (absolute_import, division, print_function)
__metaclass__ = type

import re
import os

from ansible.utils.display import Display

display = Display()


class FilterModule(object):
    """
        openjdk8u-jdk_x64_linux_hotspot_8u275b01.tar.gz
        openjdk9u-jdk_x64_linux_hotspot_9.0.4_11.tar.gz
        openjdk10u-jdk_x64_linux_hotspot_10.0.2_13.tar.gz
        openjdk11u-jdk_x64_linux_hotspot_11.0.9.1_1.tar.gz
        openjdk11u-jdk_x64_linux_hotspot_2021-01-07-17-26.tar.gz
        openjdk12u-jdk_x64_linux_hotspot_12.0.2_10.tar.gz
        openjdk13u-jdk_x64_linux_hotspot_13.0.2_8.tar.gz
        openjdk14u-jdk_x64_linux_hotspot_14.0.2_12.tar.gz
        openjdk15u-jdk_x64_linux_hotspot_15.0.1_9.tar.gz
        OpenJDK16-jdk_x64_linux_hotspot_16_36.tar.gz (PRE RELEASE!)
        OpenJDK16U-jdk_x64_linux_hotspot_16.0.1_9.tar.gz
    """

    def filters(self):
        return {
            'java_full_version': self.java_full_version,
            'java_release_version': self.java_release_version,
            'java_checksum': self.checksum,
            # 'java_version': self.parse_java_file,
        }

    def java_full_version(self, name, java_jvm, operation_system, arch):
        """
        """
        display.v("java_full_version(name, {}, {}, {})".format(java_jvm, operation_system, arch))

        result = 0

        basename = os.path.basename(name)
        # display.v(" name '{}'".format(name))
        # display.v(" basename '{}'".format(basename))
        name = basename.lower()
        # name = name.replace('%2B','_').lower()

        re_filter = re.compile(r"(?<=openjdk)(?P<major_version>[\d]+).*-(?:jdk|jre)_{1}_{0}_(?:hotspot|openj9)_(?P<full_version>.*).tar.gz$".format(operation_system, arch))

        match = re_filter.search(name)

        if match:
            major_version = match.group('major_version')
            full_version = match.group('full_version')

            display.v(" major_version '{}'".format(major_version))
            display.v(" full_version  '{}'".format(full_version))

            # version 8
            if major_version == '8':
                # return: 8u275b01
                result = full_version
            else:
                re_filter = re.compile(r"(?P<date>^\d{4}-\d{2}-\d{2}).*$")
                match = re_filter.search(full_version)

                if match:
                    # version with date
                    # return: 11.20210117
                    result = "{}.{}".format(major_version, match.group('date').replace('-', ''))
                else:
                    # return: 11.0.9.1
                    re_filter = re.compile(r"(?P<version>^[\d.]+).*$")
                    match = re_filter.search(full_version)
                    result = match.group('version')

        display.v("return '{}'".format(result))

        return result


    def java_release_version(self, name, java_jvm, operation_system, arch):
        """
        """
        display.v("java_release_version(name, {}, {}, {})".format(java_jvm, operation_system, arch))

        result = 0

        basename = os.path.basename(name)
        name = basename.lower()

        re_filter = re.compile(r"(?<=openjdk)(?P<major_version>[\d]+).*-(?:jdk|jre)_{1}_{0}_(?:hotspot|openj9)_(?P<full_version>.*).tar.gz$".format(operation_system, arch))

        match = re_filter.search(name)

        if match:
            major_version = match.group('major_version')
            full_version = match.group('full_version')

            display.v(" major_version '{}'".format(major_version))
            display.v(" full_version  '{}'".format(full_version))

            # version 8
            if major_version == '8':
                # return: 8u275b01
                result = full_version
            else:
                re_filter = re.compile(r"(?P<date>^\d{4}-\d{2}-\d{2}).*$")
                match = re_filter.search(full_version)

                if match:
                    # version with date
                    # return: 11.20210117
                    result = "{}.{}".format(major_version, match.group('date').replace('-', ''))
                else:
                    # version: 16.0.1_9
                    # result:  16.0.1%2B9
                    result = full_version.replace("_", "%2B")


        display.v("return '{}'".format(result))

        return result


    def checksum(self, data, operation_system, arch):
        """
        """
        checksum = None

        # OpenJDK11U-jdk_x64_linux_hotspot_11.0.15_10.tar.gz

        # name = data.lower()

        re_filter = fr'(?P<checksum>[0-9a-z](?:-?[0-9a-z]){{63}}).*(?<=openjdk).*-(?:jdk|jre)_{arch}_{operation_system}_(?:hotspot|openj9)_(?P<full_version>.*).tar.gz$'

        display.v(" re_filter  '{}'".format(re_filter))
        display.v(" data       '{}' {}".format(data, type(data)))

        if isinstance(data, list):
            # filter OS
            # linux = [x for x in data if re.search(r".*pushgateway-.*.{}.*.tar.gz".format(os), x)]
            # filter OS and ARCH
            checksum = [x for x in data if re.findall(re_filter, x, re.IGNORECASE)][0]

            # checksum = re.findall(re_filter, data)

        display.v(" checksum  '{}'".format(checksum))

        if isinstance(checksum, str):
            checksum = checksum.split(" ")[0]

        display.v("= checksum: {}".format(checksum))

        return checksum
