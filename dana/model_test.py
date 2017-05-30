import json

import pytest
from sqlalchemy import literal, null
from sqlalchemy.orm import aliased

from dana.walker import Collection
from dana.model import Navtree, NavtreeEncoder


def test_collection(dbsession):
    root = dbsession.query(Collection).get('2011m30')
    assert 'Szeemann' in root.label

    assert 10 == len(root.children)
    assert 'Series I.' in root.children[0].label
    assert 'Series X.' in root.children[-1].label

    curator_files = root.children[2]
    assert 'Curator' in curator_files.label
    assert curator_files.parent_slug == root.slug
    assert 3 == len(curator_files.children)


def test_collection_series_with_no_subseries(dbsession):
    root = dbsession.query(Collection).get('2011m30')
    navtree = Navtree(root)
    assert navtree.label == root.label
    assert navtree.slug == root.slug
    assert len(navtree.children) == 10
    assert len(navtree.children[0].children) == 0
    assert len(navtree.children[2].children) == 3
    assert 'Series III.' in navtree.children[2].label

    doc = json.dumps(navtree, cls=NavtreeEncoder)
    doc = json.loads(doc)
    assert 'Series I.' in doc['children'][0]['label']
    assert doc['children'][0]['children'] == []

    assert len(doc['children'][2]['children']) == 3
