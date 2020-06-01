import os
import shutil
import subprocess
import sys

class ProductBuildException(Exception):
    '''Error when creating pkg'''
    pass

def generate(info, createuserpkg_dir):
    # Hide and rename created component package
    component_pkg = os.path.dirname(info[u'destination_path']) + "/.tmp.pkg"
    shutil.move(os.path.expanduser(info[u'destination_path']), component_pkg)

    # Create distribution package
    try:
        cmd = ['/usr/bin/productbuild',
               '--package', component_pkg,
               '--identifier', info[u'pkgid'],
               '--version', info[u'version'],
               os.path.expanduser(info[u'destination_path'])
              ]
        retcode = subprocess.call(cmd)
        if retcode:
            raise PkgException('Product creation failed')
    except (OSError, IOError), err:
        raise ProductBuildException(unicode(err))
    finally:
        os.remove(component_pkg)
