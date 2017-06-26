from collections import OrderedDict
from collections import defaultdict
from collections import namedtuple
import json
import sys
import time

from salsa import Session
from sqlalchemy.sql import text

from dana.walker import Collection, Collection


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


def navtree(rows, top):
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


def gendoc(slug, dbsession):
    root = dbsession.query(Collection).get(slug)
    sql =  sqltxt('sql/navtree.bound.sql')
    rows = dbsession.execute(sql, dict(slug=slug))
    tree = navtree(rows, Node(row=root))
    fname = 'output/navtree/{}.json'.format(slug)
    with open(fname, 'w') as f:
        json.dump(tree[slug], f, indent=4, separators=(',', ': '), cls=NodeEncoder)


if __name__ == '__main__':
    dbsession = Session()
    start = time.time()
    for line in sys.stdin:
        gendoc(line.strip(), dbsession)
    delta = time.time() - start
    print('Done in {:f} seconds'.format(delta))
