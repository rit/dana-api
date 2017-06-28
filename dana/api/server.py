from flask import Flask
from flask_sqlalchemy import SQLAlchemy

from yargs import parse


settings = parse('settings')
app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = settings.dburl
db = SQLAlchemy(app)


class Collection(db.Model):
    __tablename__ = 'collections'
    __table_args__ = {
        'autoload': True,
        'autoload_with': db.engine
    }


@app.route('/navtree/<slug>')
def navtree(slug):
    collection = db.session.query(Collection).get(slug)
    return collection.label
