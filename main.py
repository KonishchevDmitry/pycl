"""Contains various functions for script bootstrapping."""

from __future__ import unicode_literals

import locale
import platform

_ENCODING = None
"""Cache of current locale's encoding."""


def system_encoding():
    """Returns system encoding."""

    global _ENCODING

    if _ENCODING is not None:
        return _ENCODING

    # There are some bugs in OS X locale settings.
    if not is_osx():
        _ENCODING = locale.getlocale()[1]

    if _ENCODING is None:
        _ENCODING = "utf-8"

    return _ENCODING


def is_osx():
    """Returns True if we are running under OS X."""

    return platform.system() == "Darwin"


def setup_environment():
    """Configures the script's environment."""

    # There are some bugs in OS X locale settings.
    if not is_osx():
        locale.setlocale(locale.LC_ALL, "")
