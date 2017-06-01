# Generate navtree json file for a collection

from collections import OrderedDict
from collections import defaultdict
from collections import namedtuple
import json
import sys
import time

from abacus.db import Session
from sqlalchemy.sql import text

from dana.walker import Collection
from dana.model import Navtree, NavtreeEncoder


# Collection = namedtuple('Collection', "slug, parent_slug, label, children")
Node = namedtuple('Node', 'row, children')


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
        child = Node(row=row, children=OrderedDict())
        parent = cur_level[child.row.parent_slug]
        append_child(parent, child)

    return root


def gendoc(slug, dbsession):
    root = dbsession.query(Collection).get(slug)
    navtree = Navtree(root)
    fname = 'output/navtree/{}.json'.format(slug)
    with open(fname, 'w') as f:
        json.dump(navtree, f, indent=4, separators=(',', ': '), cls=NavtreeEncoder)


if __name__ == '__main__':
    dbsession = Session()
    start = time.time()
    for line in sys.stdin:
        gendoc(line.strip(), dbsession)
    delta = time.time() - start
    print('Done in {:f} seconds'.format(delta))
