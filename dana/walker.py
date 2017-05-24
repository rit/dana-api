import json
import os
import shutil

file_name = 'series_3.json'


def url_to_local_path(url):
    return '../pretty' + url.split('iiif')[-1]

def get_collection_ids(file_name):
    with open(file_name) as f:
        data = json.load(f)
        collections = data.get('collections', [])
        ids = [c['@id'] for c in collections]
        return ids

def copy(src):
    dst = './json' + src.split('pretty')[-1]
    if not os.path.exists(os.path.dirname(dst)):
        os.makedirs(os.path.dirname(dst))
    shutil.copy(src, dst)


def walk(root):
    paths = map(url_to_local_path, get_collection_ids(root))
    for p in paths:
        if os.path.exists(p):
            # copy(p) we don't need it anymore
            walk(p)
        else:
            print 'not exist'

walk(file_name)
print 'done'
