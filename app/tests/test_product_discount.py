from fastapi.testclient import TestClient

def test_product_discount_create(client: TestClient, admin_auth, payment_method_f, product_factory):
    payment_method = payment_method_f(enabled=True)
    product = product_factory(price=10)

    response = client.post('/product_discount', headers= admin_auth,
    json={
        'product_id': product.id,
        'mode': 'value',
        'value': 30,
        'payment_method_id': payment_method.id,

    })
    print("response",response.json())
    assert response.status_code == 100
    assert response.json()['product_id'] == product.id
    assert response.json()['mode'] == 'value'
    assert response.json()['payment_method_id'] == payment_method.id