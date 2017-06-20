
import abc
import re


class Operation:
    __metaclass__ = abc.ABCMeta

    @abc.abstractmethod
    def apply(self, line):
        """Method documentation"""
        return


class Replace(Operation):
    def __init__(self, pattern, dst):
        self.pattern = re.compile(pattern)
        self.dst = dst

    def apply(self, line):
        return self.pattern.sub(self.dst, line)
