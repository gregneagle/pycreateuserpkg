# encoding: utf-8
# Copyright 2022 Greg Neagle.
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

'''Wrappers for Py2 vs Py3 stuff'''

from __future__ import absolute_import

def unicodify(something, encoding="UTF-8"):
    '''Makes sure the string is unicode'''
    try:
        # Python 2
        if isinstance(something, str):
            return unicode(something, encoding)
        return unicode(something)
    except NameError:
        # Python 3
        if isinstance(something, bytes):
            return str(something, encoding)
        return str(something)