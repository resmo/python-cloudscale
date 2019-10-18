from click import Group
from collections import OrderedDict
from tabulate import tabulate

class OrderedGroup(Group):
    """
    A click Group with ordered command list.
    """

    def __init__(self, name=None, commands=[], **attrs):
        Group.__init__(self, name, **attrs)
        self.commands = OrderedDict(commands)

    def list_commands(self, ctx):
        return self.commands.keys()


def to_table(data, headers):
    cols = list()
    for d in data:
        rows = list()
        for header in headers:
            if header in d:
                row = d[header]
                rows.append(row)
        cols.append(rows)

    result = tabulate(cols, headers=headers)
    return result
