
import json
from click import Group
from collections import OrderedDict
from tabulate import tabulate

class OrderedGroup(Group):
    '''
    A click Group with ordered command list.
    '''

    def __init__(self, name=None, commands=[], **attrs):
        Group.__init__(self, name, **attrs)
        self.commands = OrderedDict(commands)

    def list_commands(self, ctx):
        return self.commands.keys()


def to_table(data: list, headers: list) -> str:
    '''
    Turn a list into a table
    '''

    cols = list()
    for d in data:
        rows = list()
        for header in headers:
            if header in d:
                if header == 'tags':
                    row = ', '.join(['%s=%s' % (k, v) for k, v in d[header].items()])
                elif isinstance(d[header], dict):
                    if 'name' in d[header]:
                        row = d[header]['name']
                    elif 'slug' in d[header]:
                        row = d[header]['slug']
                    else:
                        row = d[header]
                elif isinstance(d[header], list):
                    row = ', '.join([i['slug'] for i in d[header] if 'slug' in i])
                else:
                    row = d[header]
                rows.append(row)
        cols.append(rows)

    result = tabulate(cols, headers=headers)
    return result

def to_pretty_json(data: dict) -> tuple:
    '''
    Format JSON to human readable.
    '''
    result = json.dumps(data, sort_keys=True, indent=4)
    try:
        from pygments import highlight, lexers, formatters
        result = highlight(result, lexers.JsonLexer(), formatters.TerminalFormatter())
    except ImportError:
        pass
    return result

def to_dict(data: tuple) -> dict:
    '''
    Split a tuple of tags (key=value) into a dict.
    '''
    if not data:
        return

    result = dict()
    for d in data:
        if '=' in d:
            k, v = d.split('=')
            result[k] = v
    return result
