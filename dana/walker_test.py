from .walker import slugify

def test_slugify():
    url = "http://data.getty.edu/iiif/research/archives/2011m30/collection.json"
    assert slugify(url) == '2011m30'

    url = "http://data.getty.edu/iiif/research/archives/2011.m30/collection.json"
    assert slugify(url) == '2011.m30'

    url = "http://data.getty.edu/iiif/research/archives/2011-m30/collection.json"
    assert slugify(url) == '2011-m30'

    url = "http://data.getty.edu/iiif/research/archives/2011_m30/collection.json"
    assert slugify(url) == '2011_m30'
