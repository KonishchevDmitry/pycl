"""pycl - Python core library.

This is a small set of some useful classes which I'm going to use in all my
Python projects.
"""

from __future__ import unicode_literals

import logging

class NullHandler(logging.Handler):
    def emit(self, record):
        pass

logging.getLogger("pycl").addHandler(NullHandler())
