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
        dict(slug=c.slug, label=c.label, description=c.doc.get('description', ''),
            type=c.type, metadata=c.doc.get("metadata", []))
        for c in collections
    ]
    # TODO Exclude manifests and collections from the select statement
    doc['manifests'] = []
    doc['collections'] = []
    doc['children'] = docs
    return jsonify(doc)


@app.route('/collections/<slug>')
def collection(slug):
    coll = db.session.query(Collection).get(slug)
    doc = coll.doc
    doc['_slug'] = coll.slug
    doc['_root'] = bool(doc.parent_slug)
    return jsonify(doc)


@app.route('/objects/<slug>/location')
def object_location(slug):
    sql = sqltxt('sql/location.bound.sql')
    res = db.session.execute(sql, dict(slug=slug))
    return jsonify(res.fetchall())
