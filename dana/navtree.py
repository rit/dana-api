# Generate navtree json file for a collection

import sys
import json
import time

from abacus.db import Session
from dana.walker import Collection
from dana.model import Navtree, NavtreeEncoder


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
