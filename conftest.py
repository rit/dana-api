import pytest

from abacus.testing import dbsession


pytest.fixture(dbsession)
