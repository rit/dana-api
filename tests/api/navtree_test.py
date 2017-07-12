import json

import pytest
from mock import Mock
from toolz.itertoolz import first

from dana.api.navtree import sqltxt, nav, Node, NodeEncoder
from dana.api.model import Collection
from dana.loader import load


@pytest.fixture
def sample_collection(dbsession):
    paths = [
        "dana/fixtures/collection/szeemann_collection.json",
        "dana/fixtures/collection/szeemann_series_iv_collection.json",
        "dana/fixtures/collection/szeemann_series_iv_subseries_f_collection.json"
    ]
    [load(path, dbsession) for path in paths]


def test_nav(dbsession, sample_collection):
    slug = '2011m30'
    sql =  sqltxt('sql/navtree.bound.sql')
    rows = dbsession.execute(sql, dict(slug=slug))
    row = dbsession.query(Collection).get(slug)
    top = Node(row=row)
    root = nav(rows, top)
    assert len(root) == 1

    keys = root.keys()

    root_node = root[keys[0]]
    assert len(root_node.children) == 10

    keys = root_node.children.keys()
    series1 = root_node.children[keys[0]]
    assert 'Series I.' in series1.row.label
    assert len(series1.children) == 0

    series4 = root_node.children[keys[3]]
    assert 'Series IV.' in series4.row.label
    assert len(series4.children) == 6


def test_nav_json(dbsession, sample_collection):
    slug = '2011m30'
    sql =  sqltxt('sql/navtree.bound.sql')
    rows = dbsession.execute(sql, dict(slug=slug))
    row = dbsession.query(Collection).get(slug)
    top = Node(row=row)
    tree = nav(rows, top)
    doc = json.dumps(tree, cls=NodeEncoder)
    ddoc = json.loads(doc)
    assert 'Szeemann' in ddoc[slug]['label']
    assert len(ddoc[slug]['children']) == 10

    series1 = ddoc[slug]['children'][0]
    assert 'Series I.' in  series1['label']

    series10 = ddoc[slug]['children'][9]
    assert 'Series X.' in  series10['label']


def test_node_json():
    row = Mock()
    row.slug = 'hi'
    row.label = 'label'
    node = Node(row)
    doc = json.dumps(node, cls=NodeEncoder)
    keys = json.loads(doc).keys()
    assert 'label' in keys
    assert 'slug' in keys
    assert 'children' in keys
