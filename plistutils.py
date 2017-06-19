'''plist utility functions'''

from Foundation import NSPropertyListSerialization
from Foundation import NSPropertyListXMLFormat_v1_0
from Foundation import NSPropertyListBinaryFormat_v1_0

class FoundationPlistException(Exception):
    """Basic exception for plist errors"""
    pass


def object_to_bplist(rootObject):
    '''Return 'rootObject' as a binary bplist object.'''
    plistData, error = (
        NSPropertyListSerialization.
        dataFromPropertyList_format_errorDescription_(
            rootObject, NSPropertyListBinaryFormat_v1_0, None))
    if plistData is None:
        if error:
            error = error.encode('ascii', 'ignore')
        else:
            error = "Unknown error"
        raise FoundationPlistException(error)
    else:
        return plistData


def writePlist(dataObject, filepath):
    '''
    Write 'rootObject' as a plist to filepath.
    '''
    plistData, error = (
        NSPropertyListSerialization.
        dataFromPropertyList_format_errorDescription_(
            dataObject, NSPropertyListXMLFormat_v1_0, None))
    if plistData is None:
        if error:
            error = error.encode('ascii', 'ignore')
        else:
            error = "Unknown error"
        raise FoundationPlistException(error)
    else:
        if plistData.writeToFile_atomically_(filepath, True):
            return
        else:
            raise FoundationPlistException(
                "Failed to write plist data to %s" % filepath)
