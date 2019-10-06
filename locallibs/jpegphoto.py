# Copyright 2019 Timothy Perfitt.
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

'''Functions for generating JPEGPhoto'''


import binascii
import os

def jpeg_photo_from_file(file_path):
    '''Read in a file and return binary data as ascii formatted for plist (groups of 4 bytes)'''

    photo_data=buffer("")
    if os.path.exists(file_path):
        with open(file_path,'rb') as photo_file:
            photo_data=buffer(photo_file.read())
                
    return photo_data
