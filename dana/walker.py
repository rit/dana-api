import json
import os
import re

from sqlalchemy import Table

from abacus.db import Base
from abacus.db import Session
from abacus.db import metadata


class Collection(Base):
    __table__ = Table('collections', metadata, autoload=True)


pattern = re.compile(r".+/archives/([.\w-]+)/collection.json$")


def extract_slug(url):
    matched = pattern.match(url)
    if matched:
        return matched.group(1)
    return None


def collection_slugs(doc):
    collections = doc.get('collections', [])
    pairs = [(extract_slug(c['@id']), c['label']) for c in collections]
    return pairs


def load_json(path):
    with open(path) as f:
        return json.load(f)


def walk(path, dbsession):
    doc = load_json(path)
    label = doc['label']
    slug = extract_slug(doc['@id'])
    collection = Collection(slug=slug, label=label, doc=doc)
    dbsession.add(collection)

    child_collections = collection_slugs(doc)
    for child in child_collections:
        child_slug, child_label = child
        coll = Collection(slug=child_slug, label=child_label, parent_slug=slug, doc={})
        dbsession.add(coll)

    dbsession.commit()

    # child_slugs = collection_slugs(source)

import sys

if __name__ == '__main__':
    for line in sys.stdin:
        print line.strip()
