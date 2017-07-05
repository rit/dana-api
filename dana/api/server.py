import json

from .core import app
from .core import db
from .model import Collection
from .navtree import nav, sqltxt, Node, NodeEncoder


@app.route('/navtree/<slug>')
def navtree(slug):
    root = db.session.query(Collection).get(slug)
    sql =  sqltxt('sql/navtree.bound.sql')
    rows = db.session.execute(sql, dict(slug=slug))
    tree = nav(rows, Node(row=root))
    return json.dumps(tree[slug], cls=NodeEncoder)
