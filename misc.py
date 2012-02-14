"""Miscellaneous convenient functions."""

import errno
import uuid as origin_uuid


def syscall_wrapper(func, *args, **kwargs):
    """Calls func() ignoring EINTR error."""

    while True:
        try:
            return func(*args, **kwargs)
        except EnvironmentError as e:
            if e.errno == errno.EINTR:
                pass
            else:
                raise


def uuid():
    """Generates a compact UUID."""

    return str(origin_uuid.uuid4()).replace("-", "")

