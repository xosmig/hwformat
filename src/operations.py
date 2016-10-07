
import re


class OpType:
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
