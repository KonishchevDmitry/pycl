"""Various daemon-related functions."""

from __future__ import unicode_literals

import errno
import fcntl
import os
import stat
import sys

from psys import eintr_retry

from pycl.core import Error


class PidFileLocked(Error):
    """Raised when we attempt to lock an already locked PID file."""

    def __init__(self):
        Error.__init__(self, "The PID file is already locked by another process.")


def acquire_pidfile(pid_file):
    """Opens and locks a PID file"""

    fd = -1

    try:
        fd = eintr_retry(os.open)(pid_file, os.O_RDWR | os.O_CREAT, 0600)

        if fd <= sys.stderr.fileno():
            eintr_retry(os.dup2)(fd, sys.stderr.fileno() + 1)
            eintr_retry(os.close)(fd)
            fd = sys.stderr.fileno() + 1

        try:
            fcntl.flock(fd, fcntl.LOCK_EX | fcntl.LOCK_NB)
        except EnvironmentError as e:
            if e.errno == errno.EWOULDBLOCK:
                raise PidFileLocked()
            else:
                raise e

        fd_stat = os.fstat(fd)

        try:
            file_stat = os.stat(pid_file)
        except EnvironmentError as e:
            if e.errno == errno.ENOENT:
                raise PidFileLocked()
            else:
                raise e

        if(
            ( fd_stat[stat.ST_DEV],   fd_stat[stat.ST_INO]   ) !=
            ( file_stat[stat.ST_DEV], file_stat[stat.ST_INO] )
        ):
            raise PidFileLocked()

        return fd
    except Exception as e:
        if fd != -1:
            eintr_retry(os.close)(fd)

        if isinstance(e, PidFileLocked):
            raise e

        raise Error("Failed to lock the pidfile: {0}.", e)
