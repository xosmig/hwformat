
import abc
import regex


class Operation:
    __metaclass__ = abc.ABCMeta

    @abc.abstractmethod
    def apply(self, line):
        """Method documentation"""
        return


class Replace(Operation):
    def __init__(self, pattern, dst):
        self.pattern = regex.compile(pattern)
        self.dst = dst

    def apply(self, line):
        (line, cnt) = self.pattern.subn(self.dst, line)
        return (line, cnt > 0)
