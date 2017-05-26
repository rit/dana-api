from .walker import walk
from .walker import Collection
from .walker import extract_slug


def test_walk(dbsession):
    walk('./dana/fixtures/szeemann.json', dbsession)

    all = dbsession.query(Collection).all()
    assert len(all) == 1

def test_extract_slug():
    url = "http://data.getty.edu/iiif/research/archives/2011m30/collection.json"
    assert extract_slug(url) == '2011m30'

    url = "http://data.getty.edu/iiif/research/archives/2011.m30/collection.json"
    assert extract_slug(url) == '2011.m30'

    url = "http://data.getty.edu/iiif/research/archives/2011-m30/collection.json"
    assert extract_slug(url) == '2011-m30'

    url = "http://data.getty.edu/iiif/research/archives/2011_m30/collection.json"
    assert extract_slug(url) == '2011_m30'

