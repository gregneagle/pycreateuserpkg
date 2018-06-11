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

'''Generates our user account plist'''

import uuid


class UserPlistException(Exception):
    '''Error when creating user plist'''
    pass


def generate(user_dict):
    '''Generates a local directory services user account plist'''
    user = {}
    required_keys = [u'name', u'uid', u'ShadowHashData']
    writers_keys = [u'_writers_hint', u'_writers_jpegphoto', u'_writers_passwd',
                    u'_writers_picture', u'_writers_realname',
                    u'_writers_UserCertificate']
    for key in required_keys:
        if key not in user_dict:
            raise UserPlistException(u'Missing %s!' % key)
    user[u'name'] = [user_dict[u'name']]
    user[u'uid'] = [user_dict[u'uid']]
    user[u'gid'] = [user_dict.get(u'gid', u'20')]
    user[u'home'] = [user_dict.get(u'home', u'/Users/%s' % user_dict[u'name'])]
    user[u'realname'] = [user_dict.get(u'realname', user_dict[u'name'])]
    user[u'shell'] = [user_dict.get(u'shell', u'/bin/bash')]
    user[u'generateduid'] = [user_dict.get(u'uuid', str(uuid.uuid4()).upper())]
    user[u'passwd'] = [u'********']
    user[u'authentication_authority'] = [
        ';ShadowHash;HASHLIST:<SALTED-SHA512-PBKDF2>']
    user[u'ShadowHashData'] = [user_dict['ShadowHashData']]
    for key in writers_keys:
        user[key] = [user_dict[u'name']]
    if u'image_path' in user_dict:
        user[u'picture'] = [user_dict[u'image_path']]
    if u'image_data' in user_dict:
        user[u'jpegphoto'] = [user_dict[u'image_data']]
    if u'IsHidden' in user_dict:
        user[u'IsHidden'] = [user_dict[u'IsHidden']]
    return user
