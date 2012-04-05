"""Contains various functions for script bootstrapping."""

import locale
import platform

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
    """Prepares the script's environment."""

    # There are some bugs in OS X locale settings.
    if not pycl.main.is_osx():
        pycl.main.set_locale()


def set_locale():
    """Sets current locale from environment."""

    locale.setlocale(locale.LC_ALL, "")
