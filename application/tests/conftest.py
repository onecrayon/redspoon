"""Standard pytest fixtures used across all API tests

## USAGE
    from falcon.testing import TestClient as FalconClient

    def test_health_check(client: FalconClient):
        response = client.simulate_get('/health-check')
        assert response.status == falcon.HTTP_OK
"""
import pytest
from falcon import testing

from application import app


@pytest.fixture
def client() -> testing.TestClient:
    return testing.TestClient(app)
