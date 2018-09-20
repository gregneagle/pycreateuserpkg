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

'''Functions for generating ShadowHashData'''

import hashlib

from . import arc4random
from . import pbkdf2

from . import plistutils


def make_salt(saltlen):
    '''Generate a random salt'''
    salt = ''
    for char in arc4random.randsample(0, 255, saltlen):
        salt += chr(char)
    return salt


def generate(password):
    '''Generate a ShadowHashData structure as used by macOS 10.8+'''
    iterations = arc4random.randrange(30000, 50000)
    salt = make_salt(32)
    keylen = 128
    try:
        entropy = hashlib.pbkdf2_hmac(
            'sha512', password, salt, iterations, dklen=keylen)
    except AttributeError:
        # old Python, do it a different way
        entropy = pbkdf2.pbkdf2_bin(
            password, salt, iterations=iterations, keylen=keylen,
            hashfunc=hashlib.sha512)

    data = {
        'SALTED-SHA512-PBKDF2': {
            'entropy': buffer(entropy),
            'iterations': iterations,
            'salt': buffer(salt)
        },
    }
    return plistutils.write_plist(data, plist_format='binary')
