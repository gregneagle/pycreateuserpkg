'''kcpassword encoder'''

# Port of Gavin Brock's Perl kcpassword generator to Python, by Tom Taylor
# <tom@tomtaylor.co.uk>.
# Perl version: http://www.brock-family.org/gavin/perl/kcpassword.html

# This version:
# https://gitlab.cates.io/packer/osx-vm-templates/blob/1790a91e95af3f24ca464a28297cb66d29e1b5be/scripts/support/set_kcpassword.py

import sys
import os


def generate(passwd):
    '''Given a password, generates the data for the kcpasswd file used
    by autologin.'''
    # The magic 11 bytes - these are just repeated
    # 0x7D 0x89 0x52 0x23 0xD2 0xBC 0xDD 0xEA 0xA3 0xB9 0x1F
    key = [125,137,82,35,210,188,221,234,163,185,31]
    key_len = len(key)
    block_size=key_len+1
    
    #convert to array add zero to end of password
    passwd = [ord(x) for x in list(passwd)] + [0]

    # pad passwd length out to an even multiple of block_size
    r = len(passwd) % (block_size)
    if (r > 0):
        passwd = passwd + [0] * (block_size - r)
    print passwd
    for n in range(0, len(passwd), len(key)):
        ki = 0
        for j in range(n, min(n+len(key), len(passwd))):
            passwd[j] = passwd[j] ^ key[ki]
            ki += 1

    if (len(passwd) == 0):
        passwd = [125, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]

    passwd = [chr(x) for x in passwd]
    return "".join(passwd)

