"""Miscellaneous convenient functions."""

import uuid as origin_uuid


def uuid():
    """Generates a compact UUID."""

    return str(origin_uuid.uuid4()).replace("-", "")

