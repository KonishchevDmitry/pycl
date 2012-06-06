"""Provides a class for displaying table data in the text form."""

import copy
import sys


class TextTable:
    """Can be filled up with data and draw it on a text stream."""

    __rows = None
    """Table row data."""

    def __init__(self):
        self.__rows = []


    def add_row(self, row):
        """Adds a row to the table."""

        self.__rows.append(row)


    def draw(self, headers, stream = sys.stdout, spacing = 3):
        """Prints out the table contents."""

        headers = copy.deepcopy(headers)

        first = True
        for header in headers:
            max_len = 0
            for row in self.__rows:
                max_len = max(max_len, len(unicode(row.get(header["id"]) or "")))

            header["hide"] = ( header.get("hide_if_empty", False) and max_len == 0 )
            header["max_len"] = max(max_len, len(header.get("name") or ""))

            if header["hide"]:
                continue

            if first:
                first = False
            else:
                stream.write(" " * spacing)
            stream.write(header["name"].center(header["max_len"]))

        stream.write("\n\n")

        for row in self.__rows:
            first = True
            for header in headers:
                if header["hide"]:
                    continue

                if first:
                    first = False
                else:
                    stream.write(" " * spacing)

                value = unicode(row.get(header["id"], ""))

                align = header.get("align", "right")
                if align == "left":
                    value = value.ljust(header["max_len"])
                elif align == "center":
                    value = value.center(header["max_len"])
                else:
                    value = value.rjust(header["max_len"])

                stream.write(value)
            stream.write("\n")
