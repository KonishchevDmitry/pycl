"""Contains various functions for script bootstrapping."""

# Attention! Be aware that importing something heavy here may break
# set_environment().

import codecs
import locale
import platform
import sys

import pycl.main

_ENCODING = None
"""Cache of current locale's encoding."""


def get_locale_encoding(cache = False):
    """Returns current locale's encoding."""

    # There are some bugs in OS X locale settings.
    if pycl.main.is_osx():
        return "UTF-8"

    global _ENCODING

    if cache and _ENCODING is not None:
        return _ENCODING

    _ENCODING = locale.getlocale()[1]

    if _ENCODING is None:
        _ENCODING = "UTF-8"

    return _ENCODING


def is_osx():
    """Returns True if we are running under OS X."""

    return platform.system() == "Darwin"


def set_environment():
    """Configures the script's environment."""

    # There are some bugs in OS X locale settings.
    if not pycl.main.is_osx():
        pycl.main.set_locale()

    # Configure the standart I/O streams.
    # Without this Python's logging won't be able to accept unicode data and
    # we'll have to explicitly convert all printed data to the system encoding.
    encoding = pycl.main.get_locale_encoding(cache = True)
    sys.stdin = codecs.getreader(encoding)(sys.stdin)
    sys.stdout = codecs.getwriter(encoding)(sys.stdout)
    sys.stderr = codecs.getwriter(encoding)(sys.stderr)


def set_locale():
    """Sets current locale from environment."""

    locale.setlocale(locale.LC_ALL, "")

