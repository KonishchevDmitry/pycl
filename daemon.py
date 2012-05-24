"""Various daemon-related functions."""

import errno
import fcntl
import os
import stat
import sys

from pycl.core import Error
from pycl.misc import syscall_wrapper
from pycl.misc import to_system_encoding


class PidFileLocked(Error):
    """Raised when we attempt to lock an already locked PID file."""

    def __init__(self):
        Error.__init__(self, "The PID file is already locked by another process.")


def acquire_pidfile(pid_file):
    """Opens and locks a PID file"""

    fd = -1

    try:
        fd = syscall_wrapper(os.open, to_system_encoding(pid_file),
            os.O_RDWR | os.O_CREAT, 0600)

        if fd <= sys.stderr.fileno():
            syscall_wrapper(os.dup2, fd, sys.stderr.fileno() + 1)
            syscall_wrapper(os.close, fd)
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
            file_stat = os.stat(to_system_encoding(pid_file))
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
            syscall_wrapper(os.close, fd)

        if isinstance(e, PidFileLocked):
            raise e

        raise Error("Failed to lock the pidfile: {0}.", e)
