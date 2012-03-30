"""Contains various functions for script bootstrapping."""

import locale
import platform

import pycl.main

_ENCODING = None
"""Cache of current locale's encoding."""


def get_locale_encoding(cache = False):
    """Returns current locale's encoding."""

    global _ENCODING

    if cache and _ENCODING is not None:
        return _ENCODING

    try:
        _ENCODING = locale.getlocale()[1]

        if _ENCODING is None:
            _ENCODING = "UTF-8"
    except ValueError:
        if pycl.main.is_osx():
            # There are some bugs in OS X locale settings, so just force using
            # UTF-8 encoding on errors.
            _ENCODING = "UTF-8"
        else:
            raise

    return _ENCODING


def is_osx():
    """Returns True if we are running under OS X."""

    return platform.system() == "Darwin"


def set_environment():
    """Prepares the script's environment."""

    pycl.main.set_locale()


def set_locale():
    """Sets current locale from environment."""

    locale.setlocale(locale.LC_ALL, "")
