
import re


def change_extension(filename, old_extension, new_extension):
    return re.sub(r"\." + old_extension, "." + new_extension, filename)
