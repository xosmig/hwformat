

def get_opts(argv, opts_without_value, opts_with_value):
    """Collect command-line options in a dictionary"""

    argv = argv[1:]  # remove the first argument (path to the program itself)
    opts = {}
    filename = None
    opts_allowed = True

    while argv:
        cur = argv[0]

        if cur == "--":
            opts_allowed = False
        elif cur[0] == '-' and opts_allowed:
            if cur in opts_with_value:
                if len(argv) < 1:
                    raise CLIParseError("Missing value for option '" + cur + "'")
                else:
                    opts[cur] = argv[1]
                    argv = argv[1:]
            elif cur in opts_without_value:
                opts[cur] = None
            else:
                raise CLIParseError("Unknown option: '" + cur + "'")
        elif filename is None:
            filename = cur
        else:
            raise CLIParseError("Two filenames provided: '" + filename + "' and '" + cur + "'")

        argv = argv[1:]

    if filename is None:
        raise CLIParseError("Missing filename")

    return filename, opts


class CLIParseError(Exception):
    """Exception raised for errors in the process of parsing command line arguments."""

    def __init__(self, message):
        self.message = message
