#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# (c) 2020-2022, Bodo Schulz <bodo@boone-schulz.de>

from __future__ import print_function

import os
import re

from ansible.module_utils.basic import AnsibleModule

__metaclass__ = type

ANSIBLE_METADATA = {
    'metadata_version': '0.1',
    'status': ['preview'],
    'supported_by': 'community'
}

DOCUMENTATION = """
---
module: java_version.py
author:
    - 'Bodo Schulz'
short_description: Detect installed java Version
description: Detect installed java Version
"""

EXAMPLES = """

"""


class JavaVersion(object):
    """
        Main Class
    """
    module = None

    def __init__(self, module):
        """

        """
        self.module = module
        self.java_versions = self.module.params.get("versions")
        self.install_directory = self.module.params.get("install_directory")

    def run(self):
        """

        """
        self.module.log(msg="search into: {}".format(self.install_directory))

        r = {}

        if not os.path.isdir(self.install_directory):
            return dict(
                changed=False,
                failed=False,
                msg="No installed versions of Java found."
            )

        for item in os.listdir(self.install_directory):
            self.module.log(msg="  - {}".format(item))
            binary = os.path.join(self.install_directory, item, "bin", "java")

            if (os.path.isfile(binary)):
                self.module.log(msg="    - {}".format(binary))

                rc, out, err = self._exec(
                    [binary, '-version']
                )

                date = "unknown"

                if (rc == 0):
                    # openjdk version "1.8.0_275"
                    # openjdk version "9.0.4"
                    # openjdk version "12.0.2" 2019-07-16
                    re_filter = re.compile(r'^openjdk version "(?P<version>[\d._]+)".*')
                    match = re_filter.search(err)

                if (match):
                    full_version = match.group('version')
                    version_array = full_version.split('.')
                    # self.module.log(msg="      - {}".format(version_array))
                    if (int(version_array[0]) == 1 and int(version_array[1]) == 8):
                        # == JDK8
                        major_version = version_array[1]
                    elif (int(version_array[0]) == 9):
                        # == JDK9
                        major_version = version_array[0]
                    else:
                        # > JDK9
                        re_filter = re.compile(r'^openjdk version "(?P<version>[\d.]+)" (?P<date>.*).*')
                        match = re_filter.search(err)
                        if (match):
                            major_version = version_array[0]
                            if (match.group('date')):
                                date = match.group('date')

                    r[full_version] = dict(
                        major_version=major_version,
                        full_version=full_version,
                        install_path=os.path.join(self.install_directory, item),
                        date=date
                    )

        self.module.log(msg="= {}".format(r))

        return dict(
            changed=False,
            failed=False,
            msg=r
        )

    def _exec(self, args):
        '''   '''
        # self.module.log(msg="cmd: {}".format(args))
        rc, out, err = self.module.run_command(args, check_rc=True)
        # self.module.log(msg="  rc : '{}'".format(rc))
        # self.module.log(msg="  out: '{}' ({})".format(out, type(out)))
        # self.module.log(msg="  err: '{}'".format(err))
        return rc, out, err

# ===========================================
# Module execution.
#


def main():
    """

    """
    module = AnsibleModule(
        argument_spec=dict(
            versions=dict(required=True, type=list),
            install_directory=dict(required=False, default="/opt/java"),
        ),
        supports_check_mode=True
    )

    client = JavaVersion(module)
    result = client.run()

    module.exit_json(**result)


if __name__ == '__main__':
    main()
