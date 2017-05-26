import json
import os
import re

from sqlalchemy import Table

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


def collection_slugs(doc):
    collections = doc.get('collections', []) + doc.get('manifests', [])
    vaules = [dict(slug=extract_slug(c['@id']), label=c['label'], type=c['@type']) for c in collections]
    return vaules


def load_json(path):
    with open(path) as f:
        return json.load(f)


def walk(path, dbsession):
    doc = load_json(path)
    label = doc['label']
    slug = extract_slug(doc['@id'])
    type = doc['@type']
    collection = Collection(slug=slug, label=label, type=type, doc=doc)
    dbsession.merge(collection)

    child_collections = collection_slugs(doc)
    for child in child_collections:
        coll = Collection(parent_slug=slug, doc={}, **child)
        dbsession.merge(coll)

    dbsession.commit()


import sys

if __name__ == '__main__':
    dbsession = Session()
    for line in sys.stdin:
        walk(line.strip(), dbsession)
