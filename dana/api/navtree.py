from collections import OrderedDict

from sqlalchemy.sql import text


class Node(object):
    def __init__(self, row):
        self.row = row
        self.children = OrderedDict()


def sqltxt(fpath):
    with open(fpath) as sql:
        return text(sql.read())


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
