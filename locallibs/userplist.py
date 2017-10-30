'''Generates our user account plist'''

import uuid

import shadowhash


class UserPlistException(Exception):
    '''Error when creating user plist'''
    pass


def generate(user_dict):
    '''Generates a local directory services user account plist'''
    user = {}
    REQUIRED_KEYS = [u'name', u'uid', u'ShadowHashData']
    WRITERS_KEYS = [u'_writers_hint', u'_writers_jpegphoto', u'_writers_passwd',
                    u'_writers_picture', u'_writers_realname',
                    u'_writers_UserCertificate']
    for key in REQUIRED_KEYS:
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
    for key in WRITERS_KEYS:
        user[key] = [user_dict[u'name']]
    if u'image_path' in user_dict:
        user[u'picture'] = [user_dict[u'image_path']]
    if u'image_data' in user_dict:
        user[u'jpegphoto'] = [user_dict[u'image_data']]
    if u'IsHidden' in user_dict:
        user[u'IsHidden'] = [user_dict[u'IsHidden']]
    return user
