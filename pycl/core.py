"""Core classes and function."""


class Error(Exception):
    """The base class for all exceptions that our code throws."""

    def __init__(self, error, *args):
        Exception.__init__(self, error.format(*args) if len(args) else error)


    def append(self, error, *args):
        """Appends a new error text to this error."""

        if not isinstance(error, Exception):
            error = Error(*args)
        error = EE(error)

        text = str(self).strip()

        if text:
            if text[-1] in (":", ",", ";"):
                if error:
                    if error[0].isupper() and not error[1:].isupper():
                        error = error[0].lower() + error[1:]

                    text += " " + error
                else:
                    text = text[:-1] + "."
            else:
                if text[-1] != ".":
                    text += "."

                if error:
                    text += " " + error[0].upper() + error[1:]

            if not text.endswith("."):
                text += "."
        else:
            text = error

        Exception.__init__(self, text)

        return self


class LogicalError(Error):
    """Any logical error."""

    def __init__(self):
        Error.__init__(self, "Logical error.")


def _(text, *args):
    """Stub for future gettext support."""

    return text.format(*args) if len(args) else text


def EE(e):
    """Converts an exception to a human readable string."""

    if hasattr(e, "strerror") and e.strerror:
        error = e.strerror
    else:
        error = str(e)

    if error:
        if not error[0].isupper():
            error = error[0].upper() + error[1:]

        if not error.endswith("."):
            error += "."

    return error
