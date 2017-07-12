import pytest

from salsa.testing import dbsession

from dana.loader import load


pytest.fixture(dbsession)


@pytest.fixture
def sample_collection(dbsession):
    paths = [
        "dana/fixtures/collection/szeemann_collection.json",
        "dana/fixtures/collection/szeemann_series_iv_collection.json",
        "dana/fixtures/collection/szeemann_series_iv_subseries_f_collection.json"
    ]
    [load(path, dbsession) for path in paths]
