
# python 3 headers, required if submitting to Ansible
from __future__ import print_function

import re
import os

from ansible.utils.display import Display

display = Display()

class FilterModule(object):
    """

    """

    def filters(self):
        return {
            'parse_java_version': self.parse_java_file,
        }

    def parse_java_file(self, name):
        """

        """
        result = 0
        major_version = None
        full_version = None

        display.vv(" name '{}'".format(name))
        basename = os.path.basename(name)
        display.vv(" basename '{}'".format(basename))

        name = basename.lower()

        # name = name.replace('%2B','_').lower()

        display.vv("name '{}'".format(name))

        # java-1.8.0-amazon-corretto-jdk_8.282.08-1_amd64.deb
        # java-15-amazon-corretto-jdk_15.0.2.7-1_amd64.deb
        # java-15-amazon-corretto-jdk_15.0.2.7-1_amd64.deb
        #
        # java-1.8.0-amazon-corretto-devel-1.8.0_282.b08-1.x86_64.rpm
        # java-11-amazon-corretto-devel-11.0.10.9-1.x86_64.rpm
        # java-15-amazon-corretto-devel-15.0.2.7-1.x86_64.rpm
        #
        # amazon-corretto-8.282.08.1-linux-x64.tar.gz
        # amazon-corretto-11.0.10.9.1-linux-x64.tar.gz
        # amazon-corretto-15.0.2.7.1-linux-x64.tar.gz

        re_filter = re.compile(r"java-(?P<major_version>.*)-amazon-corretto-(?P<full_version>.*)-.*$")

        match = re_filter.search(name)

        if(match):
            major_version = match.group('major_version')
            full_version = match.group('full_version')

        display.vv(" major_version '{}'".format(major_version))
        display.vv(" full_version  '{}'".format(full_version))

        if(major_version is None):
            return None


        # version 8
        if(major_version == '8'):
            # return: 8u275b01
            result = full_version
        else:
            re_filter = re.compile(r"(?P<date>^\d{4}-\d{2}-\d{2}).*$")
            match = re_filter.search(full_version)

            if(match):
                # version with date
                # return: 11.20210117
                result = "{}.{}".format(major_version, match.group('date').replace('-', ''))
            else:
                # return: 11.0.9.1
                re_filter = re.compile(r"(?P<version>^[\d.]+).*$")
                match = re_filter.search(full_version)
                result = match.group('version')

        display.vv("return '{}'".format(result))

        return result
