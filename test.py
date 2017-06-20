import kcpassword
import plistutils
import userpkg
import userplist
import shadowhash

from Foundation import NSDictionary


# Danger: this demo generates a autologin local admin user with a weak password!

password =  'testpassword'

user_data = {'name': 'test',
             'uid': '505',
             'ShadowHashData': shadowhash.generate(password)}
user_plist = userplist.generate(user_data)
# we do it this way because it most closely resembles dscl output
print NSDictionary.dictionaryWithDictionary_(user_plist)

pkg_data = {'version': '1.0',
            'pkgid': 'com.foo.test_user',
            'destination_path': '~/Desktop/test-1.0.pkg',
            'kcpassword': kcpassword.generate(password),
            'is_admin': True,
            'user_plist': user_plist}
userpkg.generate(pkg_data)