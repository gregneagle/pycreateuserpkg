#!/usr/bin/python

# Copyright 2018 Greg Neagle.
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

"""Creates a local user from a user.plist using OpenDirectory API"""

import os
import sys

# PyLint cannot properly find names inside Cocoa libraries, so issues bogus
# No name 'Foo' in module 'Bar' warnings. Disable them.
# pylint: disable=E0611
from Foundation import NSData
from Foundation import NSPropertyListSerialization
from Foundation import NSPropertyListMutableContainers
from OpenDirectory import ODSession, ODNode, kODRecordTypeUsers
# pylint: enable=E0611


def local_node():
    """Returns local DS node"""
    my_session = ODSession.defaultSession()
    if not my_session:
        return None
    node, err = ODNode.nodeWithSession_name_error_(
        my_session, "/Local/Default", None
    )
    if err:
        print >> sys.stderr, err
    return node


def get_user_record(username):
    """Returns a user record"""
    record = None
    node = local_node()
    if node:
        record, err = node.recordWithRecordType_name_attributes_error_(
            kODRecordTypeUsers,
            username,
            None,
            None
        )
        if err:
            print >> sys.stderr, err
    return record


def create_user_record(username):
    """Creates a user record"""
    record = None
    node = local_node()
    if node:
        record, err = node.createRecordWithRecordType_name_attributes_error_(
            kODRecordTypeUsers,
            username,
            None,
            None
        )
        if err:
            print >> sys.stderr, err
    return record


def set_attributes_for_user(attrs, user_record):
    """Sets user record attributes"""
    if user_record:
        for key, value in attrs.items():
            success, err = user_record.setValue_forAttribute_error_(
                value, key, None
            )
            if not success:
                print >> sys.stderr, err
                return False
        return True
    print sys.stderr, "User record was nil"
    return False


class FoundationPlistException(Exception):
    """Basic exception for plist errors"""
    pass


def read_plist(filepath):
    """
    Read a .plist file from filepath.  Return the unpacked root object
    (which is usually a dictionary).
    """
    plist_data = NSData.dataWithContentsOfFile_(filepath)
    data_object, _, error = (
        NSPropertyListSerialization.
        propertyListFromData_mutabilityOption_format_errorDescription_(
            plist_data, NSPropertyListMutableContainers, None, None))
    if data_object is None:
        if error:
            error = error.encode('ascii', 'ignore')
        else:
            error = "Unknown error"
        errmsg = "%s in file %s" % (error, filepath)
        raise FoundationPlistException(errmsg)
    else:
        return data_object


def main():
    """Our main routine"""
    try:
        username = sys.argv[1]
    except IndexError, err:
        print >> sys.stderr, "Missing a username to add!"
        exit(-1)
    this_dir = os.path.dirname(sys.argv[0])
    user_plist = "%s.plist" % username
    plist_path = os.path.join(this_dir, user_plist)
    if not os.path.exists(plist_path):
        print >> sys.stderr, "%s doesn't exist" % plist_path
        exit(-1)
    try:
        userdata = read_plist(plist_path)
    except FoundationPlistException, err:
        print >> sys.stderr, err
        exit(-1)
    record = get_user_record(username)
    if not record:
        record = create_user_record(username)
    if not record:
        print >> sys.stderr, "Failed to create user record"
        exit(-1)
    success = set_attributes_for_user(userdata, record)
    if not success:
        exit(-1)


if __name__ == '__main__':
    main()
