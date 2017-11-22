
# TODO: code blocks and inline code like in markdown
# TODO: \< and \>.
#   usecase: linear span
# TODO: easy matrices
#   possible solution: use indentation
# TODO: simple transposition
#   possible solution: (1, 1, 1, 1)\^T = a column
# mb TODO: \sub! <=> \subsetneq
# TODO: priority system instead of dependency on order of commands.
#   m.b. invent some new syntax to define operations
# TODO: inline and multiline comments (example: /*  ... anything (m.b. several lines) ... */)
# TODO: invent some cool syntax for operations on sets like \sum, \prod
#   wishlist:
#       \sum{x in A} == \sum\limits_{x \in A}
#       \sum{x !in A} == \sum\limits_{x \not\in A}
#       \sum{j /= k} == \sum\limits_{x \neq k}
#       \sum{j in [a..b]} == \sum\limits_{x = a}^{b}
#       multiple counters:
#           \sum{x, y in [a..b]} == \sum\limits_{x, y \in A}
#           \sum{x in A}{y in B} == \sum\limits_{x \in A; y \in B}
# TODO: variables:
#   examples:
#       SA := \sum{x in A} foo(x)
#   some kind of scopes (headers)
# TODO: easy pictures insertion
#   possible solution: like in markdown
# TODO: convert to pdf
#   possible solution: use subprocess
# TODO: ability to modify headers.
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

import sys
import patterns
import target
import resources
from operations import *
from cli_parser import *
from utils import *


OPERATIONS_BEFORE_MATH = [
    # trim extra spaces in the end of line:
    Replace(r"[ ]+$", ""),

    # comments:
    Replace("//.*$", ""),

    # skips:
    Replace(r"^\-\-\-+\n$", r"@\\medskip\n"),
    Replace(r"^===+\n$", r"@\\bigskip\n"),

    # @\undef\foo command
    Replace(r"\\undef(\\[a-zA-Z0-9]+)", r"\\let\1\\undefined"),

    # backslash: \\ and newline: \n
    Replace(r"\\\\", r"\\textbackslash{}"),
    Replace(r"\\n([^a-zA-Z])", r"\\\\\1"),

    # emphasis: italic text: //text//
    Replace(r"\*/(.*?)/\*", r"\\textit{\1}"),

    # bold text: **text**
    Replace(r"\*\*(.*?)\*\*", r"\\textbf{\1}"),

    # underlined text: __text__
    Replace(r"__(.*?)__", r"\\underline{\1}"),

    # dash
    # Warning: must go earlier than russian text parsing
    Replace(r" \-\- ", r"\\text{ -- }"),

    # wrap russian in text block:
    Replace(patterns.RUS_WORD, r"\\text{\1}\\allowbreak "),
]

OPERATIONS_AFTER_MATH = [
    # open math mode in the begin of a line:
    Replace(r"^(#*)", r"\1\\("),
    # close math mode in the end of a line:
    Replace(r"(\n$)", r"\\)\1"),

    # headers:
    Replace(r"^(@?)####(.*)(\n$)", r"\1\\medskip\\textbf{\2}\\medskip\3"),
    Replace(r"^(@?)###(.*)(\n$)", r"\1\\subsubsection*{\2}\3"),
    Replace(r"^(@?)##(.*)(\n$)", r"\1\\subsection*{\2}\3"),
    Replace(r"^(@?)#(.*)(\n$)", r"\1\\section*{\2}\3"),
]

OPERATIONS_MATH_RECURSIVE = [
    # arrows
    Replace("<=>", r"\\Leftrightarrow "),
    Replace("<==>", r"\\Leftrightarrow "),
    Replace("==>", r"\\Rightarrow "),
    Replace("<==", r"\\Leftarrow "),
    Replace("\-\->", r"\\rightarrow "),
    Replace("<\-\-", r"\\leftarrow "),

    # two kinds of not_equal operators
    Replace("!=", r"\\neq "),
    Replace("/=", r"\\neq "),

    # comparison operators
    Replace("<=", r"\\le "),
    Replace(">=", r"\\ge "),

    # equals sign with three lines
    Replace("==", r"\\equiv "),
    # equals symbol with ~ (isomorphism)
    Replace("~=", "\\cong "),

    # ~ over a text
    Replace(patterns.TILDE_OVER, r"\\widetilde "),
    # line over a text
    Replace(patterns.OVERLINE, r"\\overline "),

    # plus-minus symbol
    Replace(r"\+\-", r"\\pm "),

    # not operator. example: \!in == \not\in
    # also "empty set" and "not exist" symbols
    Replace(r"\\!O", r"\\varnothing"),
    Replace(r"\\!E", r"\\nexists"),
    Replace(r"\\!", r"\\not\\"),

    # division [[! numerator / denominator ]] and [[ numerator / denominator ]]
    Replace(r"\[\[!([^][]*)\/([^][]*)\]\]", r"\\cfrac{\1}{\2}"),
    Replace(patterns.DIVISION, r"\\frac{\1}{\2}"),

    # star symbol: \* and multiply: *
    Replace(r"[^\\]\*", r"\\cdot "),
    Replace(r"\\\*", r"*"),

    # text entry:
    Replace(r"([^[]?)\[\{", r"\1\\text{"),
    Replace(r"\}\]([^]]?)", r"}\1"),

    # ranges:
    Replace(r"{(.+?) in "+patterns.RANGE+r"}", r"_{\1 = \2}^{\3}"),
]


# TODO: get header path to the parameters
def hw_to_tex(filename, output_file=None, header_file=None):
    """None value for output_file means default output file name.
    If no header provided, the default one will be used."""

    if output_file is None:
        output_file = change_extension(filename, "hw", "tex")

    with open(output_file, "w") as dest:
        if header_file is None:
            dest.write(resources.DEFAULT_HEADER)
        else:
            dest.writelines(open(header_file, "r").readlines())

        dest.write("\n\\begin{document}\n")

        with open(filename, "r") as source:
            for line in source.readlines():
                for op in OPERATIONS_BEFORE_MATH:
                    (line, ok) = op.apply(line)

                if line.startswith("@"):
                    # cut the raw_operator out
                    line = line[1:]
                elif line != "\n":
                    # if line isn't empty nor comment:`
                    while True:
                        op_performed = False
                        for op in OPERATIONS_MATH_RECURSIVE:
                            (line, ok) = op.apply(line)
                            op_performed |= ok
                        if not op_performed:
                            break

                for op in OPERATIONS_AFTER_MATH:
                    (line, ok) = op.apply(line)

                dest.write(line)

        dest.write("\n\\end{document}\n")


def main():
    # project_dir = path.pardir(path.dirname(path.realpath(__file__)))

    help_option_names = ["h", "-h", "help", "-help", "--help", "?", "-?"]
    if len(sys.argv) == 1 or (len(sys.argv) == 2 and sys.argv[1] in help_option_names):
        print(resources.HELP_MESSAGE)

    output_option = CLIOptionWithValue(["-o", "-output", "--output"])
    header_option = CLIOptionWithValue(["-h", "-header", "--header"])
    try:
        filename, opts = get_opts(sys.argv, [output_option, header_option])
    except CLIParseError as err:
        sys.stderr.write("Parse error: " + err.message + "\n")
        exit(2)
    else:
        hw_to_tex(filename, output_option.value)

if __name__ == "__main__":
   main()
