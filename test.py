import pkg
import shadowhash
import userplist

shadow_hash_data = shadowhash.generate('SEKRET')
user_dict = {'name': 'temp', 'uid': '502', 'ShadowHashData': shadow_hash_data}
user_plist = userplist.generate(user_dict)

pkg_info = {'name': 'temp', 'version': '1.0', 'pkgid': 'com.foo.temp_user',
            'destination_path': '~/Desktop/temp-1.0.pkg'}
pkg.generate(pkg_info, user_plist)