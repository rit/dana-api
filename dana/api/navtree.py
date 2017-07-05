from collections import OrderedDict
import json
import sys
import time

from sqlalchemy.sql import text

from .model import Collection


class Node(object):

    def __init__(self, row):
        self.row = row
        self.children = OrderedDict()


class NodeEncoder(json.JSONEncoder):

    def default(self, obj):

        if isinstance(obj, Node):
            # obj.row can be RowProxy or Collection
            return dict(label=obj.row.label, slug=obj.row.slug,
                    children=obj.children.values())

        return json.JSONEncoder.default(self, obj)


def sqltxt(fpath):
    with open(fpath) as f:
        return text(f.read())


def append_child(root, node):
    root.children[node.row.slug] = node
    return root


def nav(rows, top):
    root = OrderedDict()
    root[top.row.slug] = top
    cur_level = root
    depth = 1
    parent = None
    for row in rows:
        if row.depth > depth:
            depth += 1
            cur_level = parent.children
        child = Node(row)
        parent = cur_level[child.row.parent_slug]
        append_child(parent, child)

    return root
