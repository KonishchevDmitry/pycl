"""Miscellaneous convenient functions."""

from __future__ import unicode_literals

import errno
import uuid as origin_uuid

import pycl.main


def to_system_encoding(string):
    """Converts a string to system encoding if it's a unicode object."""

    if isinstance(string, unicode):
        return string.encode(pycl.main.system_encoding())
    else:
        return string


def to_unicode(string):
    """Converts a string to a Unicode string if it's not a unicode object."""

    if isinstance(string, unicode):
        return string
    else:
        return string.decode(pycl.main.system_encoding())


def uuid():
    """Generates a compact UUID."""

    return unicode(origin_uuid.uuid4()).replace("-", "")

