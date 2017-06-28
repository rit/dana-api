import json

from mock import Mock
from toolz.itertoolz import first

from dana.navtree import sqltxt, navtree, Node, NodeEncoder
from dana.loader import Collection


def test_navtree(dbsession):
    slug = '2011m30'
    sql =  sqltxt('sql/navtree.bound.sql')
    rows = dbsession.execute(sql, dict(slug=slug))
    row = dbsession.query(Collection).get(slug)
    top = Node(row=row)
    root = navtree(rows, top)
    assert len(root) == 1

    keys = root.keys()

    root_node = root[keys[0]]
    assert len(root_node.children) == 10

    keys = root_node.children.keys()
    series1 = root_node.children[keys[0]]
    assert 'Series I.' in series1.row.label
    assert len(series1.children) == 0

    series3 = root_node.children[keys[2]]
    assert 'Series III.' in series3.row.label
    assert len(series3.children) == 3


def test_navtree_json(dbsession):
    slug = '2011m30'
    sql =  sqltxt('sql/navtree.bound.sql')
    rows = dbsession.execute(sql, dict(slug=slug))
    row = dbsession.query(Collection).get(slug)
    top = Node(row=row)
    tree = navtree(rows, top)
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
