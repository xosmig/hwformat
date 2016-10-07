
# TODO: custom latex header support
# TODO: convert to pdf
#   possible solution: use subprocess
# TODO: parsing command line arguments
# TODO: headers (#)
# TODO: lists (enumerated and not enumerated, nested)
# TODO: division (common, nested)
# TODO: help message
# TODO: complex example with definition
# TODO: good default header
# TODO: inline comments
# FIXME: problem with spaces in math mode
#   possible solutions:
#   + m.b. that's ok.
#   + interpret all spaces as spaces and don't let latex remove them.

import re
import sys
import patterns
import target
import resources
from operations import OpType, Operation

FORMAT = "hw"

OPERATIONS = [
    # trim extra spaces in the end of line
    Operation(OpType.replace, r"[ ]+$", ""),
    # comments.
    Operation(OpType.replace, patterns.LINE_COMMENT, target.LINE_COMMENT),
]

OPERATIONS_MATH = [
    # wrap russian in text block:
    Operation(OpType.replace, patterns.RUS_WORD, r"\\text{\1}\\allowbreak "),
    # warning: <=> should be parsed before => and <=
    Operation(OpType.replace, "<=>", r"\\Leftrightarrow "),
    Operation(OpType.replace, "=>", r"\\Rightarrow "),
    # two kinds of not_equal operators
    Operation(OpType.replace, "!=", r"\\neq "),
    Operation(OpType.replace, "/=", r"\\neq "),
    # comparison operators
    Operation(OpType.replace, "<=", r"\\le "),
    Operation(OpType.replace, ">=", r"\\ge "),
    # arrows
    Operation(OpType.replace, "\->", r"\\rightarrow "),
    Operation(OpType.replace, "<\-", r"\\leftarrow "),
    # equals sign with three lines
    Operation(OpType.replace, "==", r"\\equiv "),
    # equals symbol with ~ (isomorphism)
    Operation(OpType.replace, patterns.ISOMORPHIC, "\\cong "),
    # ~ over a text
    Operation(OpType.replace, patterns.TILDE_OVER, r"\\widetilde "),
    # line over a text
    Operation(OpType.replace, patterns.OVERLINE, r"\\overline "),
    # plus-minus symbol
    Operation(OpType.replace, r"\+\-", r"\\pm "),
    # not operator
    Operation(OpType.replace, "\\\\" + patterns.NOT, r"\\not\\"),
    # TODO: division
    # -e 's/$(LEFT)\/$(RIGHT)/\\frac{\1}{\2}/g' \
    # multiply
    Operation(OpType.replace, r"\*", r"\\cdot "),
    # non-math block inline:
    Operation(OpType.replace, patterns.NON_MATH_OPEN, target.MATH_CLOSE),
    Operation(OpType.replace, patterns.NON_MATH_CLOSE, target.MATH_OPEN),
]


def main():
    if len(sys.argv) != 2:
        print("TODO: Help message")
        exit(1)

    source_path = sys.argv[1]
    dest_path = re.sub(r"\." + FORMAT, r".tex", source_path)  # FIXME
    header = resources.DEFAULT_HEADER

    with open(dest_path, "w") as dest:
        dest.write(header)
        dest.write("\n\\begin{document}\n")

        with open(source_path, "r") as source:
            for line in source.readlines():
                for op in OPERATIONS:
                    line = op.do(line)

                if line.startswith(patterns.RAW):
                    # cut the raw_operator out
                    line = line[len(patterns.RAW):]
                elif line != "\n" and not line.startswith(target.LINE_COMMENT):
                    # if line isn't empty nor comment:

                    for op in OPERATIONS_MATH:
                        line = op.do(line)

                    line = target.MATH_OPEN + line

                    # place close_math operator before end of line
                    line = re.sub("\n$", target.MATH_CLOSE + r"\n", line)

                dest.write(line)

        dest.write("\n\\end{document}\n")


if __name__ == "__main__":
    main()
