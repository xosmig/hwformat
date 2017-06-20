
import abc


def get_opts(argv, options):
    """Collect command-line options in a dictionary"""

    argv = argv[1:]  # remove the first argument (path to the program itself)
    opts = set()
    filename = None
    opts_allowed = True

    while argv:
        token = argv[0]

        if token == "--":
            opts_allowed = False
        elif token[0] == '-' and opts_allowed:
            try:
                option = next(option for option in options if token in option.names)
            except StopIteration:
                raise CLIParseError("Unknown option: '" + token + "'")
            opts.add(option)
            if isinstance(option, CLIOptionWithValue):
                try:
                    option.value = argv[1]
                    argv = argv[1:]
                except IndexError:
                    raise CLIParseError("Missing value for option '" + token + "'")
        elif filename is None:
            filename = token
        else:
            raise CLIParseError("Two filenames provided: '" + filename + "' and '" + token + "'")

        argv = argv[1:]

    if filename is None:
        raise CLIParseError("Missing filename")

    return filename, opts


class CLIOption:
    def __init__(self, names):
        self.names = names


class CLIOptionWithValue(CLIOption):
    def __init__(self, names):
        super().__init__(names)
        self.value = None


class CLIParseError(Exception):
    """Exception raised for errors in the process of parsing command line arguments."""

    def __init__(self, message):
        self.message = message
