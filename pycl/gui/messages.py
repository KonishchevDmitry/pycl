"""Provides functions for displaying GUI messages."""

from __future__ import unicode_literals

from PySide import QtCore, QtGui

from pycl.core import EE


_DIALOGS = []
"""
Keeps references to dialogs which have no parent to prevent destroying of them
by GC.
"""


def error(parent, title, message, block = True):
    """Shows an error message blocking on it until user close it."""

    return _message(parent, QtGui.QMessageBox.Critical, title, message, block)


def warning(parent, title, message, block = True):
    """Shows a warning message blocking on it until user close it."""

    return _message(parent, QtGui.QMessageBox.Warning, title, message, block)


def _message(parent, type, title, message, block):
    """Shows a message of specified type blocking on it until user close it."""

    if isinstance(title, Exception):
        title = EE(title)

    if isinstance(message, Exception):
        message = EE(message)

    message_box = QtGui.QMessageBox()
    message_box.setTextFormat(QtCore.Qt.PlainText)
    message_box.setWindowTitle(title)
    message_box.setText(message)
    message_box.setIcon(type)

    if block:
        message_box.exec_()
    else:
        message_box.show()

        _DIALOGS.append(message_box)
        message_box.finished.connect(lambda: _DIALOGS.remove(message_box))
