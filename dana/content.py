# Generate content json file for a collection

import sys
import json
import time

from abacus.db import Session 
from dana.walker import Collection


def gendoc(slug, dbsession):
    collections = dbsession.query(Collection).filter_by(parent_slug=slug).all()
    docs = [
        dict(slug=c.slug, label=c.label, metadata=c.doc["metadata"])
        for c in collections
    ]
    fname = 'output/content/{}.json'.format(slug)
    with open(fname, 'w') as f:
        json.dump({ "collections": docs }, f, indent=4, separators=(',', ': '))


if __name__ == '__main__':
    dbsession = Session()
    start = time.time()
    for line in sys.stdin:
        gendoc(line.strip(), dbsession)
    delta = time.time() - start
    print('Done in {:f} seconds'.format(delta))
