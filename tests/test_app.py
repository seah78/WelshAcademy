from tests.conftest import *

def test_home(client):
    response = client.get('/')
    assert response.status_code == 200
    assert b"Welsh Academy" in response.data
    assert b"Welsh Academy's API site." in response.data