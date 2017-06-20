import kcpassword
import pkg
import shadowhash
import userplist

# Danger: this demo generates a autologin local admin user with a weak password!

shadow_hash_data = shadowhash.generate('testpassword')
kcp = kcpassword.generate('testpassword')

user_dict = {'name': 'test', 'uid': '505', 'ShadowHashData': shadow_hash_data}
user_plist = userplist.generate(user_dict)

pkg_info = {'name': 'test', 'version': '1.0', 'pkgid': 'com.foo.test_user',
            'destination_path': '~/Desktop/test-1.0.pkg', 'kcpassword': kcp,
            'is_admin': True, 'user_plist': user_plist}
pkg.generate(pkg_info)