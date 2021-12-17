from fastapi.testclient import TestClient

def test_adress_create(client: TestClient):
    response = client.post('/adress', json={'name': None})
    assert response.status_code == 201
    assert response.json()['id'] == 1