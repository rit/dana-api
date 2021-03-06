from __future__ import print_function
from itertools import count
import json
import re
import sys
import time

from sqlalchemy import Table
from sqlalchemy.dialects.postgresql import insert

from salsa import Base
from salsa import Session
from salsa import metadata


class Collection(Base):
    __table__ = Table('collections', metadata, autoload=True)


pattern = re.compile(r".+/archives/([.\w-]+)/(collection|manifest).json$")


def extract_slug(url):
    matched = pattern.match(url)
    if matched:
        return matched.group(1)


def children_collection(doc):
    collections = doc.get('collections', []) + doc.get('manifests', [])
    step = count()
    kws = [
        dict(slug=extract_slug(c['@id']), position=next(step), label=c['label'], type=c['@type'])
        for c in collections
    ]
    return kws


def load_json(path):
    with open(path) as f:
        return json.load(f)


def load(path, dbsession):
    doc = load_json(path)
    label = doc['label']
    slug = extract_slug(doc['@id'])
    type_ = doc['@type']
    upsert_data = dict(slug=slug, label=label, type=type_, doc=doc)
    insert_data = upsert_data.copy()
    insert_data.update(parent_slug=None)
    root = insert(Collection).values(insert_data)
    root = root.on_conflict_do_update(
        constraint='collections_pkey',
        # We update every columns except 'parent_slug'
        set_=dict(upsert_data))
    dbsession.execute(root)
    dbsession.commit()

    upsert_children(doc, slug, dbsession)


def upsert_children(doc, parent_slug, dbsession):
    pairs = [dict(parent_slug=parent_slug, **kw) for kw in children_collection(doc)]
    if pairs:
        sql = insert(Collection).values(pairs)
        sql = sql.on_conflict_do_update(
            constraint='collections_pkey',
            # We only update the parent slug and position
            set_=dict(parent_slug=sql.excluded.parent_slug, position=sql.excluded.position))
        dbsession.execute(sql)
        dbsession.commit()


if __name__ == '__main__':
    sess = Session()
    start = time.time()

    if len(sys.argv) > 1:
        with open(sys.argv[1]) as lines:
            for line in lines:
                print('Loading  {}'.format(line))
                load(line.strip(), sess)
        delta = time.time() - start
        print('Done in {:f} seconds'.format(delta))
    else:
        print('please provide the manifests.txt')
