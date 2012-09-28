"""
Implements all logic that is needed in ordinary Python programs for setting up
UNIX signal handlers.
"""

from __future__ import unicode_literals

import logging
import signal

from PySide import QtCore

LOG = logging.getLogger("pycl.signals")


class _UnixSignalDispatcher(QtCore.QObject):
    """
    Object that receives the UNIX signals and transmits them to other objects
    connected to it.
    """

    received = False
    """True if we've received any UNIX signal."""

    signal_received = QtCore.Signal(int)
    """Emitted when we receive a UNIX signal."""


    def __init__(self, parent = None):
        super(_UnixSignalDispatcher, self).__init__(parent)


    def signal(self, signum):
        LOG.debug("%s UNIX signal received.", signum)
        self.received = True
        self.signal_received.emit(signum)


_DISPATCHER = _UnixSignalDispatcher()
"""
Object that receives the UNIX signals and transmits them to other objects
connected to it.
"""


def connect(slot):
    """
    Connects a slot that handles UNIX signals to the UNIX signal
    dispatcher.
    """

    return _DISPATCHER.signal_received.connect(slot, QtCore.Qt.QueuedConnection)


def received():
    """Returns True if we've received any deadly UNIX signal."""

    return _DISPATCHER.received


def setup():
    """Sets up UNIX signal handlers."""

    signal.signal(signal.SIGINT, lambda signum, frame: _DISPATCHER.signal(signum))
    signal.siginterrupt(signal.SIGINT, False)

    signal.signal(signal.SIGTERM, lambda signum, frame: _DISPATCHER.signal(signum))
    signal.siginterrupt(signal.SIGTERM, False)

    signal.signal(signal.SIGQUIT, lambda signum, frame: _DISPATCHER.signal(signum))
    signal.siginterrupt(signal.SIGQUIT, False)

    signal.signal(signal.SIGCHLD, signal.SIG_IGN)
    signal.siginterrupt(signal.SIGCHLD, False)
    signal.siginterrupt(signal.SIGPIPE, False)
