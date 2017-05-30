import json

from abacus.db import Session
from dana.walker import Collection


class Navtree(object):

    def __init__(self, collection):
        self.label = collection.label
        self.slug = collection.slug
        if len(collection.children) < 21:
            self.children = map(Navtree, collection.children)
        else:
            self.children = []


class NavtreeEncoder(json.JSONEncoder):

    def default(self, obj):
        if isinstance(obj, Navtree):
            return dict(label=obj.label, slug=obj.slug, children=obj.children)

        return json.JSONEncode.default(self, obj)
