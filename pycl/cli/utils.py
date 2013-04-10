"""Various command line utils."""

def question_user(question, *args, **kwargs):
    """Questions user. Returns True if user says yes."""

    answer = ""
    while answer not in ("y", "n"):
        answer = input((question + " (y/n) ").format(*args, **kwargs))

    return answer == "y"
