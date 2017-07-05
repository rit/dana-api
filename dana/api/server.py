from .core import app
from .core import db
from .model import Collection


@app.route('/navtree/<slug>')
def navtree(slug):
    collection = db.session.query(Collection).get(slug)
    return collection.label
