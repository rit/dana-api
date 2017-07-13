from operator import attrgetter

from dana.loader import load
from dana.loader import Collection
from dana.loader import extract_slug

szeemann_slug = '2011m30'
series_slug = '2011m30_ref5903_vld'


def test_load_doc(dbsession):
    load('./dana/fixtures/szeemann.json', dbsession)
    res = dbsession.query(Collection).get(szeemann_slug)
    assert 'Szeemann' in res.label
    assert res.slug == szeemann_slug
    assert res.parent_slug is None
    assert szeemann_slug in res.doc['@id']

    children = dbsession.query(Collection).filter_by(parent_slug=szeemann_slug).all()
    assert len(children) == 10
    assert filter(bool, (map(attrgetter('doc'), children))) == []
    assert set(map(attrgetter('parent_slug'), children)) == set([szeemann_slug])
    assert len(set(map(attrgetter('slug'), children))) == 10


def test_load_doc_update(dbsession):
    count = dbsession.query(Collection).count()
    assert count == 0

    load('./dana/fixtures/szeemann.json', dbsession)
    load('./dana/fixtures/szeemann_dup.json', dbsession)
    res = dbsession.query(Collection).get(szeemann_slug)
    assert 'upserted' in res.label

    children = dbsession.query(Collection).filter_by(parent_slug=szeemann_slug).all()
    assert len(children) == 10

    load('./dana/fixtures/szeemann.json', dbsession)
    series = dbsession.query(Collection).get(series_slug)
    assert 'Series I' in series.label
    assert szeemann_slug == series.parent_slug


def test_load_doc_child_update(dbsession):
    count = dbsession.query(Collection).count()
    assert count == 0

    load('./dana/fixtures/szeemann.json', dbsession)
    load('./dana/fixtures/series.json', dbsession)
    series = dbsession.query(Collection).get(series_slug)
    assert 'Series I' in series.label
    assert szeemann_slug == series.parent_slug
    children = dbsession.query(Collection).filter_by(parent_slug=szeemann_slug).all()
    assert len(children) == 10


def test_load_doc_child_update_before_parent(dbsession):
    count = dbsession.query(Collection).count()
    assert count == 0

    load('./dana/fixtures/series.json', dbsession)
    load('./dana/fixtures/szeemann.json', dbsession)
    load('./dana/fixtures/series.json', dbsession)
    load('./dana/fixtures/szeemann.json', dbsession)
    series = dbsession.query(Collection).get(series_slug)
    assert 'Series I' in series.label
    assert szeemann_slug == series.parent_slug
    children = dbsession.query(Collection).filter_by(parent_slug=szeemann_slug).all()
    assert len(children) == 10

    series = dbsession.query(Collection).get('2011m30_ref5903_vld')
    assert 'Series I' in series.label
    assert series.parent_slug == '2011m30'
    assert series_slug in series.doc['@id']


def test_extract_slug():
    url = "http://data.getty.edu/iiif/research/archives/2011m30/collection.json"
    assert extract_slug(url) == '2011m30'

    url = "http://data.getty.edu/iiif/research/archives/2011.m30/collection.json"
    assert extract_slug(url) == '2011.m30'

    url = "http://data.getty.edu/iiif/research/archives/2011-m30/collection.json"
    assert extract_slug(url) == '2011-m30'

    url = "http://data.getty.edu/iiif/research/archives/2011_m30/collection.json"
    assert extract_slug(url) == '2011_m30'
