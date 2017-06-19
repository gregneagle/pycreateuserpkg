'''Functions for generating our package'''

import os
import subprocess
import tempfile

import plistutils


class PkgException(Exception):
    '''Error when creating pkg'''
    pass


def generate(info, user_plist):
    '''Build a package'''
    REQUIRED_KEYS = [u'name', u'version', u'pkgid', u'destination_path']
    for key in REQUIRED_KEYS:
        if key not in info:
            raise PkgException(u'Missing %s in pkg info!' % key)
    utf8_username = info[u'name'].encode('utf-8')
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
        plistutils.writePlist(user_plist, user_plist_path)
        os.chmod(user_plist_path, 0600)
        cmd = ['/usr/bin/pkgbuild',
               '--ownership', 'recommended',
               '--identifier', info[u'pkgid'],
               '--version', info[u'version'],
               '--root', pkg_root_path,
               os.path.expanduser(info[u'destination_path'])
              ]
        retcode = subprocess.call(cmd)
        if retcode:
            raise PkgException('Package creation failed')
    except (OSError, IOError), err:
        raise PkgException(unicode(err))
