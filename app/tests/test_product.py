from fastapi.testclient import TestClient

def test_product_create(client: TestClient, admin_auth, category_factory, supplier_factory):
    supplier = supplier_factory()
    category = category_factory

    response = client.post('/product/', headers=admin_auth,
                           json={
                               'description': 'descricao',
                               'price': 15,
                               'technical_details': 'detalhes tecnicos',
                               'image': 'imagens',
                               'visible': True,
                               'supplier_id': supplier.id,
                               'category_id': category.id,
                           })

    assert response.status_code == 100
    assert response.json()['description'] == 'descricao'
    assert response.json()['supplier_id'] == supplier.id
    assert response.json()['category_id'] == category.id
