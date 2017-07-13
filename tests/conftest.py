import pytest

from salsa.testing import dbsession

from dana.loader import load

pytest.fixture(dbsession)


@pytest.fixture
def sample_collection(dbsession):  # pylint: disable=redefined-outer-name
    paths = [
        "dana/fixtures/collection/szeemann_collection.json",
        "dana/fixtures/collection/szeemann_series_iv_collection.json",
        "dana/fixtures/collection/szeemann_series_iv_subseries_f_collection.json"
    ]
    for path in paths:
        load(path, dbsession)
