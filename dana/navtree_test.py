from collections import OrderedDict
from dana.navtree import sqltxt, navtree, Node
from dana.walker import ContentCollection

def test_navtree(dbsession):
    slug = '2011m30'
    sql =  sqltxt('sql/navtree.bound.sql')
    rows = dbsession.execute(sql, dict(slug=slug))
    row = dbsession.query(ContentCollection).get(slug)
    top = Node(row=row, children=OrderedDict())
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
