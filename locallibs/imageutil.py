# Copyright 2018 Gerd Niemetz.
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

'''Generates a base64 encoded JPEG from an image file'''

import imghdr
import base64
import subprocess
import os
from Foundation import NSData

class ImageUtilException(Exception):
    '''Error when generating jpeg'''
    pass

def is_non_zero_file(fpath):
    return os.path.isfile(fpath) and os.path.getsize(fpath) > 0

def generate(image_path):
    try:
        # check if image_path is an image
        if imghdr.what(image_path) is None:
            raise ImageUtilException(u'"{0}" is not a valid picture'.format(image_path))
        # build temporary image file
        temp_image = os.path.join(os.path.sep, 'private/var/tmp',
                                  os.path.splitext(os.path.basename(image_path))[0] + '.jpg')
        # convert image_path to jpeg with 72 dpi and max. width/height 512 px
        cmd = ['/usr/bin/sips',
               '-s', 'format', 'jpeg', image_path,
               '-s', 'formatOptions', 'high',
               '-s', 'dpiHeight', '72',
               '-s', 'dpiWidth', '72',
               '--resampleHeightWidthMax', '512',
               '--out', temp_image
              ]
        try:
            retcode = subprocess.call(cmd)
            if retcode:
                raise ImageUtilException(u'sips command failed')
            # check if temporary image exists and is not blank
            if is_non_zero_file(temp_image):
                with open(temp_image, 'rb') as image_file:
                    # convert temporary image to a base64 encoded string
                    return NSData.alloc().initWithBase64EncodedString_options_(
                        base64.b64encode(image_file.read()),
                        0)
            else:
                raise ImageUtilException(u'Could not convert "{0}" to a jpeg file)'.format(image_path))
        finally:
            if os.path.exists(temp_image):
                os.unlink(temp_image)
    except IOError as e:
        raise ImageUtilException(u'Cannot open "{0}" (I/O error {1}: {2})'.format(
            image_path,
            e.errno,
            e.strerror))
