import pytest

from salsa.testing import dbsession


pytest.fixture(dbsession)
