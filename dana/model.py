import json

from abacus.db import Session
from dana.walker import Collection


class Navtree(object):

    def __init__(self, collection, level=0):
        self.label = collection.label
        self.slug = collection.slug
        if level < 2 and len(collection.children) < 21:
            level += 1
            self.children = [Navtree(child, level) for child in collection.children]
        else:
            self.children = []


class NavtreeEncoder(json.JSONEncoder):

    def default(self, obj):
        if isinstance(obj, Navtree):
            return dict(label=obj.label, slug=obj.slug, children=obj.children)

        return json.JSONEncode.default(self, obj)
