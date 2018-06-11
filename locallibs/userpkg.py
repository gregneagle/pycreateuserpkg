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
import sys
import tempfile

from . import plistutils


class PkgException(Exception):
    '''Error when creating pkg'''
    pass


def make_config_file(scripts_path, pkg_info):
    """Write out a config file the postinstall script can source"""
    user_plist = pkg_info['user_plist']
    username = user_plist[u'name'][0].encode('utf-8')
    uuid = user_plist[u'generateduid'][0]
    user_is_admin = pkg_info.get('is_admin', False)
    enable_autologin = (pkg_info.get('kcpassword') != None)
    config_content = """
USERNAME="%s"
UUID=%s
USER_IS_ADMIN=%s
ENABLE_AUTOLOGIN=%s
""" % (username, uuid, user_is_admin, enable_autologin)
    config_path = os.path.join(scripts_path, "config")
    try:
        fileref = open(config_path, 'w')
        fileref.write(config_content)
        fileref.close()
        os.chmod(config_path, 0755)
    except (OSError, IOError), err:
        raise PkgException(unicode(err))


def generate(info):
    '''Build a package'''
    required_keys = [
        u'version', u'pkgid', u'destination_path', u'user_plist']
    for key in required_keys:
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
        # Create package structure inside root for psuedo-payload-free pkg
        os.makedirs(os.path.join(pkg_root_path, "private/tmp"))
        os.chmod(os.path.join(pkg_root_path, "private/tmp"), 01777)
        # Create scripts directory
        scripts_path = os.path.join(tmp_path, 'scripts')
        os.makedirs(scripts_path, 0755)
        # Save user plist.
        user_plist_name = "%s.plist" % utf8_username
        user_plist_path = os.path.join(scripts_path, user_plist_name)
        plistutils.write_plist(info[u'user_plist'], pathname=user_plist_path)
        os.chmod(user_plist_path, 0600)
        # Save kcpassword.
        if info.get('kcpassword'):
            kcpassword_path = os.path.join(scripts_path, 'kcpassword')
            fileref = open(kcpassword_path, 'w')
            fileref.write(info.get('kcpassword'))
            fileref.close()
            os.chmod(kcpassword_path, 0600)
        # now the config file
        make_config_file(scripts_path, info)
        # now copy postinstall and create_user.py to scripts dir
        # pkg_scripts should be in the same directory as createuserpkg
        createuserpkg_dir = os.path.dirname(sys.argv[0])
        pkg_scripts_dir = os.path.join(createuserpkg_dir, 'pkg_scripts')
        for script in ['create_user.py', 'postinstall']:
            source = os.path.join(pkg_scripts_dir, script)
            dest = os.path.join(scripts_path, script)
            shutil.copyfile(source, dest)
            os.chmod(dest, 0755)
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
