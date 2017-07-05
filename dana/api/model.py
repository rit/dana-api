from .core import db


class Collection(db.Model):
    __tablename__ = 'collections'
    __table_args__ = {
        'autoload': True,
        'autoload_with': db.engine
    }
