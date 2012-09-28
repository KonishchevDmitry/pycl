"""Various command line utils."""

from __future__ import unicode_literals

from pycl.misc import to_system_encoding

def question_user(question, *args, **kwargs):
    """Questions user. Returns True if user says yes."""

    answer = ""
    while answer not in ("y", "n"):
        answer = raw_input(to_system_encoding(
            (question + " (y/n) ").format(*args, **kwargs)))

    return answer == "y"
