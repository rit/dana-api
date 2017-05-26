from __future__ import print_function
import json
import os
import re
import sys
import time


from sqlalchemy import Table
from sqlalchemy.dialects.postgresql import insert


from abacus.db import Base
from abacus.db import Session
from abacus.db import metadata


class Collection(Base):
    __table__ = Table('collections', metadata, autoload=True)


pattern = re.compile(r".+/archives/([.\w-]+)/(collection|manifest).json$")


def extract_slug(url):
    matched = pattern.match(url)
    if matched:
        return matched.group(1)
    return None


def children_collection(doc):
    collections = doc.get('collections', []) + doc.get('manifests', [])
    kws = [ dict(slug=extract_slug(c['@id']), label=c['label'], type=c['@type'])
            for c in collections]
    return kws


def load_json(path):
    with open(path) as f:
        return json.load(f)


def walk(path, dbsession):
    doc = load_json(path)
    label = doc['label']
    slug = extract_slug(doc['@id'])
    type = doc['@type']
    collection = dict(slug=slug, label=label, type=type, doc=doc)
    root = insert(Collection).values(collection)
    root = root.on_conflict_do_update(
                constraint='collections_pkey',
                set_=dict(slug=root.excluded.slug))
    dbsession.execute(root)
    dbsession.commit()

    colls = [
        dict(parent_slug=slug, doc={}, **kw)
        for kw in children_collection(doc)
    ]
    if len(colls):
        sql = insert(Collection).values(colls)
        stmt = sql.on_conflict_do_update(
            constraint='collections_pkey',
            set_=dict(slug=sql.excluded.slug)
        )
        dbsession.execute(stmt)
        dbsession.commit()


if __name__ == '__main__':
    dbsession = Session()
    start = time.time()
    for line in sys.stdin:
        walk(line.strip(), dbsession)
    delta = time.time() - start
    print('Done in {:f} seconds'.format(delta))
