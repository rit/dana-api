import json

from dana.api.serializer import ModelEncoder
from dana.api.model import Collection
from dana.api.navtree import Node


def test_mapper(dbsession, sample_collection):
    res = dbsession.query(Collection).get('2011m30')
    payload = json.dumps(res, cls=ModelEncoder)
    collection = json.loads(payload)
    assert 'Szeemann' in collection['label']


def test_row_proxy(dbsession, sample_collection):
    sql = 'select * from collections where slug = :slug'
    res = dbsession.execute(sql, dict(slug='2011m30')).fetchone()
    payload = json.dumps(res, cls=ModelEncoder)
    collection = json.loads(payload)
    assert 'Szeemann' in collection['label']


def test_navtree_node(dbsession, sample_collection):
    sql = 'select * from collections where slug = :slug'
    root = dbsession.execute(sql, dict(slug='2011m30')).fetchone()
    node = Node(row=root)
    payload = json.dumps(node, cls=ModelEncoder)
    collection = json.loads(payload)
    assert 'Szeemann' in collection['label']
