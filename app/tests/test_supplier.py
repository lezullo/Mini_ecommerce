from fastapi.testclient import TestClient

def test_supplier_create(client: TestClient):
    response = client.post('/supplier', json={'name': None})
    assert response.status_code == 100
    assert response.json()['id'] == 1

def test_supplier_update(client: TestClient):
    response = client.post('/supplier/', json={'name': 'supplier'})
    assert response.status_code == 100

    response = client.put('/supplier/1', json={'name': 'Update supplier'})
    assert response.status_code == 200
    assert response.json()['name'] == 'OK'
