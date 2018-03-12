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

'''Functions for generating our package'''

# Much borrowed from https://github.com/MagerValp/CreateUserPkg/

import os
import shutil
import subprocess
import tempfile

import plistutils


POSTINSTALL_TEMPLATE = """#!/bin/bash
#
# postinstall for local account install
_POSTINSTALL_REQUIREMENTS_
_POSTINSTALL_ACTIONS_
if [ "$3" == "/" ]; then
    # we're operating on the boot volume
_POSTINSTALL_LIVE_ACTIONS_
fi
exit 0
"""

PI_REQ_PLIST_FUNCS = """
PlistArrayAdd() {
    # Add $value to $array_name in $plist_path, creating if necessary
    local plist_path="$1"
    local array_name="$2"
    local value="$3"
    local old_values
    local item
    
    old_values=$(/usr/libexec/PlistBuddy -c "Print :$array_name" "$plist_path" 2>/dev/null)
    if [[ $? == 1 ]]; then
        # Array doesn't exist, create it
        /usr/libexec/PlistBuddy -c "Add :$array_name array" "$plist_path"
    else
        # Array already exists, check if array already contains value
        IFS=$'\\012' 
        for item in $old_values; do
            unset IFS
            if [[ "$item" =~ ^\\ *$value$ ]]; then
                # Array already contains value
                return 0
            fi
        done
        unset IFS
    fi
    # Add item to array
    /usr/libexec/PlistBuddy -c "Add :$array_name: string \\"$value\\"" "$plist_path"
}
"""

PI_ADD_ADMIN_GROUPS = """
ACCOUNT_TYPE=ADMIN # Used by read_package.py.
PlistArrayAdd "$3/private/var/db/dslocal/nodes/Default/groups/admin.plist" users "_USERNAME_" && \\
    PlistArrayAdd "$3/private/var/db/dslocal/nodes/Default/groups/admin.plist" groupmembers "_UUID_"
"""

PI_ENABLE_AUTOLOGIN = """
if [ "$3" == "/" ] ; then
    # work around path issue with 'defaults'
    /usr/bin/defaults write "/Library/Preferences/com.apple.loginwindow" autoLoginUser "_USERNAME_"
else
    /usr/bin/defaults write "$3/Library/Preferences/com.apple.loginwindow" autoLoginUser "_USERNAME_"
fi
/bin/chmod 644 "$3/Library/Preferences/com.apple.loginwindow.plist"
"""

PI_LIVE_KILLDS = """
    # kill local directory service so it will see our local
    # file changes -- it will automatically restart
    /usr/bin/killall DirectoryService 2>/dev/null || /usr/bin/killall opendirectoryd 2>/dev/null
"""

PI_CREATEHOMEDIR = """
    /usr/sbin/createhomedir -c
"""

def make_postinstall_script(scripts_path, pkg_info):
    # Create postinstall script.
    try:
        user_plist = pkg_info['user_plist']
        os.makedirs(scripts_path, 0755)
        pi_reqs = set()
        pi_actions = set()
        pi_live_actions = set()
        pi_live_actions.add(PI_LIVE_KILLDS)
        if pkg_info.get('is_admin'):
            pi_actions.add(PI_ADD_ADMIN_GROUPS)
            pi_reqs.add(PI_REQ_PLIST_FUNCS)
        if pkg_info.get('kcpassword'):
            pi_actions.add(PI_ENABLE_AUTOLOGIN)
        if pkg_info.get('createhomedir'):
            pi_live_actions.add(PI_CREATEHOMEDIR)
        postinstall = POSTINSTALL_TEMPLATE
        postinstall = postinstall.replace(
            '_POSTINSTALL_REQUIREMENTS_', '\n'.join(pi_reqs))
        postinstall = postinstall.replace(
            '_POSTINSTALL_ACTIONS_', '\n'.join(pi_actions))
        postinstall = postinstall.replace(
            '_POSTINSTALL_LIVE_ACTIONS_', '\n'.join(pi_live_actions))
        postinstall = postinstall.replace(
            '_USERNAME_', user_plist[u'name'][0].encode('utf-8'))
        postinstall = postinstall.replace(
            '_UUID_', user_plist[u'generateduid'][0])
        postinstall_path = os.path.join(scripts_path, 'postinstall')
        f = open(postinstall_path, 'w')
        f.write(postinstall)
        f.close()
        os.chmod(postinstall_path, 0755)
    except (OSError, IOError), err:
        raise PkgException(unicode(err))


class PkgException(Exception):
    '''Error when creating pkg'''
    pass


def generate(info):
    '''Build a package'''
    REQUIRED_KEYS = [
        u'version', u'pkgid', u'destination_path', u'user_plist']
    for key in REQUIRED_KEYS:
        if key not in info:
            raise PkgException(u'Missing %s in pkg info!' % key)
    utf8_username = info.get(
        u'name', info[u'user_plist'][u'name'][0]).encode('utf-8')
    # Create a package with the plist for our user and a shadow hash file.
    tmp_path = tempfile.mkdtemp()
    try:
        # Create a root for the package.
        pkg_root_path = os.path.join(tmp_path, "create_user")
        os.mkdir(pkg_root_path)
        # Create package structure inside root.
        os.makedirs(os.path.join(
            pkg_root_path, "private/var/db/dslocal/nodes"), 0755)
        os.makedirs(os.path.join(
            pkg_root_path, "private/var/db/dslocal/nodes/Default/users"), 0700)
        # Save user plist.
        user_plist_name = "%s.plist" % utf8_username
        user_plist_path = os.path.join(
            pkg_root_path, 'private/var/db/dslocal/nodes/Default/users',
            user_plist_name)
        plistutils.write_plist(info[u'user_plist'], pathname=user_plist_path)
        os.chmod(user_plist_path, 0600)
        # Save kcpassword.
        if info.get('kcpassword'):
            os.makedirs(os.path.join(pkg_root_path, 'private/etc'), 0755)
            kcpassword_path = os.path.join(
                pkg_root_path, 'private/etc/kcpassword')
            f = open(kcpassword_path, 'w')
            f.write(info.get('kcpassword'))
            f.close()
            os.chmod(kcpassword_path, 0600)
        # now the postinstall script
        scripts_path = os.path.join(tmp_path, 'scripts')
        make_postinstall_script(scripts_path, info)
        cmd = ['/usr/bin/pkgbuild',
               '--ownership', 'recommended',
               '--identifier', info[u'pkgid'],
               '--version', info[u'version'],
               '--root', pkg_root_path,
               '--scripts', scripts_path,
               os.path.expanduser(info[u'destination_path'])
              ]
        retcode = subprocess.call(cmd)
        if retcode:
            raise PkgException('Package creation failed')
    except (OSError, IOError), err:
        raise PkgException(unicode(err))
    finally:
        shutil.rmtree(tmp_path, ignore_errors=True)
