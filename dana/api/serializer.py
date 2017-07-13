from flask.json import JSONEncoder
from sqlalchemy.engine.result import RowProxy

from .navtree import Node


class ModelEncoder(JSONEncoder):
    # pylint: disable=method-hidden
    def default(self, obj):
        if isinstance(obj, Node):
            # obj.row can be RowProxy or Collection
            return dict(label=obj.row.label, slug=obj.row.slug, children=obj.children.values())
        if isinstance(obj, RowProxy):
            return dict(obj.items())
        if hasattr(obj, '__mapper__'):
            return {k: getattr(obj, k) for k in obj.__mapper__.c.keys()}
        return JSONEncoder.default(self, obj)
