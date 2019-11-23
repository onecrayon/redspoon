import falcon
from falcon.testing import TestClient as FalconClient


def test_health_check(client: FalconClient):
    response = client.simulate_get('/health-check')
    assert response.status == falcon.HTTP_OK
    assert response.json.get('status') == 'okay'
