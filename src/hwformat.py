
# TODO: priority system instead of dependency on order of commands.
#   m.b. invent some new syntax to define operations
# TODO: inline and multiline comments (example: /*  ... anything (m.b. several lines) ... */)
# TODO: invent some cool syntax for operations on sets like \sum, \prod
#   wishlist:
#       \sum{x in A} == \sum\limits_{x \in A}
#       \sum{x !in A} == \sum\limits_{x \!in A}
#       \sum{j /= k} == \sum\limits_{x /= k}
#       \sum{j in [0..n]} == \sum\limits_{x = 0}^{n}
#       multiple counters
# TODO: variables:
#   examples:
#       SA := \sum{x in A} foo(x)
#   some kind of scopes (headers)
# TODO: convert to pdf
#   possible solution: use subprocess
# TODO: parse command line arguments
#   + -t --tex      - produce only .tex file (and only .pdf file otherwise)
#   + -o --output   - specify an output file
# TODO: lists (enumerated and not enumerated, nested)
# TODO: division (common, nested)
# TODO: help message
# FIXME: Now it's very hard to deal with latex error. It refers to a line in .tex file.
# TODO: example with a definition of all features
# TODO: good default header
# TODO: inline comments
# FIXME: problem with spaces in math mode
#   possible solutions:
#   + m.b. that's ok.
#   + interpret all spaces as spaces and don't let latex remove them.
# TODO: installation for windows and linux
# TODO: adopt for english language

import re
import sys
import patterns
import target
import resources
from operations import OpType, Operation

FORMAT = "hw"

OPERATIONS_BEFORE_MATH = [
    # trim extra spaces in the end of line:
    Operation(OpType.replace, r"[ ]+$", ""),

    # comments:
    # FIXME: works only in the beginning of the line
    Operation(OpType.replace, "^//", target.LINE_COMMENT),

    # skips:
    Operation(OpType.replace, r"^\-\-\-+\n$", r"@\\medskip\n"),
    Operation(OpType.replace, r"^===+\n$", r"@\\bigskip\n"),

    # @\redef\foo\bar command
    Operation(OpType.replace, r"\\redef(\\[a-zA-Z0-9]+)\{(.*)\}", r"\\undef\1 \\def\1{\2}"),
    # @\undef\foo command
    Operation(OpType.replace, r"\\undef(\\[a-zA-Z0-9]+)", r"\\let\1\\undefined"),

    # backslash: \\ and newline: \n
    Operation(OpType.replace, r"\\\\", r"\\textbackslash{}"),
    Operation(OpType.replace, r"\\n([^a-zA-Z])", r"\\\\\1"),
]

OPERATIONS_AFTER_MATH = [
    # headers:
    Operation(OpType.replace, r"^(@?)####(.*)(\n$)", r"\1\\medskip\\textbf{\2}\\medskip\3"),
    Operation(OpType.replace, r"^(@?)###(.*)(\n$)", r"\1\\subsubsection*{\2}\3"),
    Operation(OpType.replace, r"^(@?)##(.*)(\n$)", r"\1\\subsection*{\2}\3"),
    Operation(OpType.replace, r"^(@?)#(.*)(\n$)", r"\1\\section*{\2}\3"),
]

OPERATIONS_MATH = [
    # dash
    # Warning: must go earlier than russian text parsing
    Operation(OpType.replace, r" \-\- ", r"\\t{ -- }"),

    # wrap russian in text block:
    Operation(OpType.replace, patterns.RUS_WORD, r"\\text{\1}\\allowbreak "),

    # WARNING: <=> should be parsed before => and <=
    Operation(OpType.replace, "<=>", r"\\Leftrightarrow "),
    Operation(OpType.replace, "=>", r"\\Rightarrow "),

    # two kinds of not_equal operators
    Operation(OpType.replace, "!=", r"\\neq "),
    Operation(OpType.replace, "/=", r"\\neq "),

    # comparison operators
    Operation(OpType.replace, "<=", r"\\le "),
    Operation(OpType.replace, ">=", r"\\ge "),

    # arrows
    Operation(OpType.replace, "\-\->", r"\\rightarrow "),
    Operation(OpType.replace, "<\-\-", r"\\leftarrow "),
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

    # beautiful empty-set symbol:
    Operation(OpType.replace, r"\\!O", r"\\varnothing"),

    # not operator. example: \!in == \not\in
    Operation(OpType.replace, r"\\!", r"\\not\\"),

    # division
    # FIXME: временная заглушка. TODO: нормальное деление со вложенностью
    Operation(OpType.replace, r"\[\[([^][]*)\/([^][]*)\]\]", r"\\frac{\1}{\2}"),

    # star symbol: \* and multiply: *
    Operation(OpType.replace, r"[^\\]\*", r"\\cdot "),
    Operation(OpType.replace, r"\\\*", r"*"),

    # open math mode in the begin of a line:
    Operation(OpType.replace, r"^(#*)", r"\1" + target.MATH_OPEN),
    # close math mode in the end of a line:
    Operation(OpType.replace, r"(\n$)", target.MATH_CLOSE + r"\1"),

    # text entry:
    Operation(OpType.replace, r"([^[]?)\[\{", r"\1\\text{"),
    Operation(OpType.replace, r"\}\]([^]]?)", r"}\1"),
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
                for op in OPERATIONS_BEFORE_MATH:
                    line = op.do(line)

                if line.startswith("@"):
                    # cut the raw_operator out
                    line = line[1:]
                elif line != "\n" and not line.startswith(target.LINE_COMMENT):
                    # if line isn't empty nor comment:

                    for op in OPERATIONS_MATH:
                        line = op.do(line)

                for op in OPERATIONS_AFTER_MATH:
                    line = op.do(line)

                dest.write(line)

        dest.write("\n\\end{document}\n")


if __name__ == "__main__":
    main()
