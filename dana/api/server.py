from flask import jsonify
from sqlalchemy import select

from .core import app
from .core import db
from .model import Collection
from .navtree import nav, sqltxt, Node
from .serializer import ModelEncoder

app.json_encoder = ModelEncoder


@app.route('/navtree/<slug>')
def navtree(slug):
    root = db.session.query(Collection).get(slug)
    # TODO use sqlalchemy instead of raw sql
    sql = sqltxt('sql/navtree.bound.sql')
    rows = db.session.execute(sql, dict(slug=slug))
    tree = nav(rows, Node(row=root))
    return jsonify(tree[slug])


@app.route('/collectiontree/<slug>')
def collectiontree(slug):
    doc = db.session.query(Collection).get(slug).doc
    collections = db.session.query(Collection)\
            .filter_by(parent_slug=slug).order_by('position')
    docs = [
        dict(slug=c.slug, label=c.label, metadata=c.doc.get("metadata", [])) for c in collections
    ]
    # TODO Exclude manifests and collections from the select statement
    doc['manifests'] = []
    doc['collections'] = []
    doc['children'] = docs
    return jsonify(doc)


@app.route('/collections/<slug>')
def collection(slug):
    doc = db.session.query(Collection).get(slug).doc
    return jsonify(doc)


@app.route('/objects/<slug>/location')
def object_location(slug):
    c = Collection.__table__.columns
    coll = select(c).where(c.slug == slug).cte(recursive=True)
    coll_alias = coll.alias()
    parents = Collection.__table__.alias()
    coll = coll.union_all(select(parents.c).where(parents.c.slug == coll_alias.c.parent_slug))
    sql = select(coll.c).order_by(coll.c.slug)
    res = db.session.execute(sql)
    #TODO return only what needed for the UI
    return jsonify(res.fetchall())
