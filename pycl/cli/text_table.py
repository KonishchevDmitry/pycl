"""Provides a class for displaying table data in the text form."""

import codecs
import copy
import sys

from pycl.main import system_encoding


class TextTable:
    """Can be filled up with data and draw it on a text stream."""

    __rows = None
    """Table row data."""

    def __init__(self):
        self.__rows = []


    def add_row(self, row):
        """Adds a row to the table."""

        self.__rows.append(row)


    def draw(self, headers, stream = None, spacing = 3):
        """Prints out the table contents."""

        headers = copy.deepcopy(headers)

        if stream is None:
            stream = codecs.getwriter(system_encoding())(sys.stdout)

        rows = copy.deepcopy(self.__rows)
        row_lines = [ 1 ] * len(rows)

        first_visible = True
        for header in headers:
            max_len = 0
            for row_id, row in enumerate(rows):
                cell = unicode(row[header["id"]]) if header["id"] in row else ""
                cell_lines = self.__get_cell_lines(cell, max_width = header.get("max_width"))
                row[header["id"]] = cell_lines

                row_lines[row_id] = max(row_lines[row_id], len(cell_lines))
                max_len = reduce(
                    lambda max_len, line: max(max_len, len(line)),
                    cell_lines, max_len)

            header["hide"] = ( header.get("hide_if_empty", False) and max_len == 0 )
            header["max_len"] = max(max_len, len(header.get("name") or ""))

            if header["hide"]:
                continue

            if first_visible:
                first_visible = False
            else:
                stream.write(" " * spacing)
            stream.write(header["name"].center(header["max_len"]))

        stream.write("\n\n")

        for row_id, row in enumerate(rows):
            for line_id in xrange(0, row_lines[row_id]):
                first_visible = True
                for header in headers:
                    if header["hide"]:
                        continue

                    if first_visible:
                        first_visible = False
                    else:
                        stream.write(" " * spacing)

                    cell_lines = row[header["id"]]
                    cell_line = cell_lines[line_id] if line_id < len(cell_lines) else ""

                    align = header.get("align", "right")
                    if align == "left":
                        cell_line = cell_line.ljust(header["max_len"])
                    elif align == "center":
                        cell_line = cell_line.center(header["max_len"])
                    else:
                        cell_line = cell_line.rjust(header["max_len"])

                    stream.write(cell_line)
                stream.write("\n")


    def __get_cell_lines(self, cell, max_width = None):
        """Formats a cell according to header requirements."""

        lines = []

        for source_line in cell.split("\n"):
            line = ""

            for word in source_line.split(" "):
                if (
                    max_width is not None and line and
                    len(line) + 1 + len(word) > max_width
                ):
                    lines.append(line)
                    line = ""

                if line:
                    line += " "
                line += word

            lines.append(line)

        return lines
