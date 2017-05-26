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
    slugs = [extract_slug(c['@id']) for c in collections]
    return slugs


def load_json(path):
    with open(path) as f:
        return json.load(f)


def walk(path, dbsession):
    doc = load_json(path)
    label = doc['label']
    slug = extract_slug(doc['@id'])
    collection = Collection(slug=slug, label=label, doc=doc)
    dbsession.add(collection)
    dbsession.commit()

    # child_slugs = collection_slugs(source)

import sys

if __name__ == '__main__':
    for line in sys.stdin:
        print line.strip()
