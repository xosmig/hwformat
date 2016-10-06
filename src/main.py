
# TODO: separate project files
# TODO: latex header
# TODO: convert to tex
# TODO: convert to pdf
# TODO: parsing command line arguments
# TODO: headers (#)
# TODO: lists (enumerated and not enumerated, nested)
# TODO: division (common, nested)
# TODO: help message
# TODO: complex example

import sys
import re
from enum import Enum

FORMAT = "hw"


class OpType(Enum):
    # Behaves like sed 's/pattern/dst/g'.
    replace = 1
    # Behaves like sed '/pattern/d'. Removes line if pattern is found.
    remove = 2


class Operation:
    def __init__(self, tp, pattern, dst=""):
        self.type = tp
        self.pattern = re.compile(pattern)
        self.dst = dst

    def do(self, line):
        if self.type == OpType.replace:
            line = self.pattern.sub(self.dst, line)
        elif self.type == OpType.remove:
            if self.pattern.search(line) is not None:
                line = ""
        return line


class Src:
    raw = "@"
    non_math_open = r"\[\{"
    non_math_close = r"\}\]"
    comment_open = r"/\*"
    comment_close = r"\*/"
    line_comment = "//"


class Tar:
    math_open = "\\("
    math_close = "\\)"
    line_comment = r"%"
    comment_open = r"\\ignore{"
    comment_close = r"}"


def main():
    if len(sys.argv) != 2:
        print("TODO: Help message")
        exit(1)

    operations = [
        # trim extra spaces in the end of line
        Operation(OpType.replace, r"[ ]+$", ""),
        # comments.
        Operation(OpType.replace, Src.line_comment, Tar.line_comment),
    ]

    operations_math = [
        # wrap russian in text block:
        Operation(OpType.replace, "( ?[а-яА-ЯёЁ]+ ?)", r"\\text{\1}\\allowbreak"),
        # warning: <=> should be parsed before => and <=
        Operation(OpType.replace, "<=>", r"\\Leftrightarrow"),
        Operation(OpType.replace, "=>", r"\\Rightarrow"),
        # two kinds of not_equal operators
        Operation(OpType.replace, "!=", r"\\neq"),
        Operation(OpType.replace, "/=", r"\\neq"),
        # comparison operators
        Operation(OpType.replace, "<=", r"\\le"),
        Operation(OpType.replace, ">=", r"\\ge"),
        # arrows
        Operation(OpType.replace, "\->", r"\\rightarrow"),
        Operation(OpType.replace, "<\-", r"\\leftarrow"),
        # equivalence with three lines
        Operation(OpType.replace, "==", r"\\equiv"),
        # ~ under symbol text. Particularly ~= is an isomorphism symbol
        Operation(OpType.replace, "~", r"\\widetilde "),
        # plus-minus symbol
        Operation(OpType.replace, r"\+\-", r"\\pm"),
        # TODO: division
        # -e 's/$(LEFT)\/$(RIGHT)/\\frac{\1}{\2}/g' \
        # FIXME: can be used only in math mode:
        Operation(OpType.replace, Src.comment_open, Tar.math_close + Tar.comment_open),
        Operation(OpType.replace, Src.comment_close, Tar.comment_close + Tar.math_open),
        # multiply
        Operation(OpType.replace, r"\*", r"\\cdot"),
        # non-math block inline:
        Operation(OpType.replace, Src.non_math_open, Tar.math_close),
        Operation(OpType.replace, Src.non_math_close, Tar.math_open),
    ]

    file_path = sys.argv[1]

    with open(file_path, "r") as source:
            with open(re.sub(r"\." + FORMAT, r".tex", file_path), "w") as dest:
                for line in source.readlines():
                    for op in operations:
                        line = op.do(line)

                    if line.startswith(Src.raw):
                        line = line[len(Src.raw):]  # cut the raw_operator out
                    elif line != "\n" and not line.startswith(Tar.line_comment):
                        # if line isn't empty nor comment:

                        for op in operations_math:
                            line = op.do(line)

                        # TODO: header support
                        # if is_header(line):
                        #     line = re.sub(r"^(#+)", r"\1" + Tar.math_open, line)
                        # else:
                        line = Tar.math_open + line

                        # place close_math operator before end of line
                        line = re.sub("\n$", Tar.math_close + r"\n", line)

                    dest.write(line)


if __name__ == "__main__":
    main()
