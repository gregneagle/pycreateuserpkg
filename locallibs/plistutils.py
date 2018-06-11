# Copyright 2017 Greg Neagle.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#      http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

'''plist utility functions'''

# PyLint cannot properly find names inside Cocoa libraries, so issues bogus
# No name 'Foo' in module 'Bar' warnings. Disable them.
# pylint: disable=E0611
from Foundation import NSPropertyListSerialization
from Foundation import NSPropertyListXMLFormat_v1_0
from Foundation import NSPropertyListBinaryFormat_v1_0
# pylint: enable=E0611


class FoundationPlistException(Exception):
    """Basic exception for plist errors"""
    pass


def write_plist(data_object, pathname=None, plist_format=None):
    '''
    Write 'rootObject' as a plist to pathname or return as a string.
    '''
    if plist_format == 'binary':
        plist_format = NSPropertyListBinaryFormat_v1_0
    else:
        plist_format = NSPropertyListXMLFormat_v1_0

    plist_data, error = (
        NSPropertyListSerialization.
        dataFromPropertyList_format_errorDescription_(
            data_object, plist_format, None))
    if plist_data is None:
        if error:
            error = error.encode('ascii', 'ignore')
        else:
            error = "Unknown error"
        raise FoundationPlistException(error)
    if pathname:
        if plist_data.writeToFile_atomically_(pathname, True):
            return
        else:
            raise FoundationPlistException(
                "Failed to write plist data to %s" % pathname)
    else:
        return plist_data
