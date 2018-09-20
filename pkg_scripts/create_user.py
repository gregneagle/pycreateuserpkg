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


def major_darwin_version():
    '''Returns an integer with the current major Darwin version'''
    return int(os.uname()[2].split('.')[0])


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


def set_attributes_for_user(attrs, user_record, attrs_to_skip=None):
    """Sets user record attributes"""
    if attrs_to_skip is None:
        attrs_to_skip = []
    if user_record:
        for attr, value in attrs.items():
            if attr not in attrs_to_skip:
                success, err = user_record.setValue_forAttribute_error_(
                    value, attr, None
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
        # get path to user plist from first argument
        user_plist = sys.argv[1]
    except IndexError, err:
        print >> sys.stderr, "Missing path to user plist!"
        exit(-1)
    if not os.path.exists(user_plist):
        print >> sys.stderr, "%s doesn't exist!" % user_plist
        exit(-1)
    try:
        # read the user plist
        userdata = read_plist(user_plist)
    except FoundationPlistException as err:
        print >> sys.stderr, "Could not read plist: %s" % err
        exit(-1)
    try:
        # extract the username from the user plist data
        username = userdata["name"][0]
    except (KeyError, IndexError) as err:
        print >> sys.stderr, "Could not get username from plist: %s" % err
        exit(-1)
    # find a local user record for username
    record = get_user_record(username)
    attrs_to_skip = None
    if not record:
        # create a new local user named username
        record = create_user_record(username)
        if not record:
            print >> sys.stderr, "Failed to create user record!"
            exit(-1)
    else:
        # existing user record we're updating
        if major_darwin_version() >= 18:
            # Mojave prevents us from updating these attributes without
            # user approval
            attrs_to_skip = ['uid', 'home']
    success = set_attributes_for_user(
        userdata, record, attrs_to_skip=attrs_to_skip)
    if not success:
        exit(-1)


if __name__ == '__main__':
    main()
