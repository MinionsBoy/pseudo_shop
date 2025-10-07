import pytest
from app import products
from tests.utils.api_helpers import get_cart_items, post_product_to_cart
def test_post_cart_add_product(client, app):
    with app.app_context():
        product_id = 3
        price = next((p['price'] for p in products if p['id'] == product_id), 0)

    response = post_product_to_cart(client, product_id)
    assert response.status_code == 201
    assert response.is_json
    assert response.headers['Content-Type'].startswith('application/json')
    data = response.get_json()
    assert 'added' in data.get('message', '') or 'success' in data.get('message', '')

    # Add another product and check cart (edge: multiple add)
    post_product_to_cart(client, product_id)
    cart_response = client.get('/api/cart')
    assert cart_response.status_code == 200
    assert cart_response.headers['Content-Type'].startswith('application/json')
    cart = cart_response.get_json()
    assert isinstance(cart, dict)
    items = get_cart_items(cart_response)
    found = False
    for item in items:
        prod = item.get('product', item)
        if prod['id'] == product_id:
            assert item.get('quantity', 1) == 2
            found = True
    assert found
    assert 'total' in cart
    assert cart['total'] == 2 * price

def test_post_cart_missing_product_id(client):
    response = client.post('/api/cart', json={}, follow_redirects=True)
    assert response.status_code == 400
    assert response.is_json
    assert response.headers['Content-Type'].startswith('application/json')
    data = response.get_json()
    assert 'error' in data or 'message' in data

def test_post_cart_invalid_product_id_type(client):
    response = client.post('/api/cart', json={'product_id': 'not_an_int'}, follow_redirects=True)
    assert response.status_code == 400
    assert response.is_json
    assert response.headers['Content-Type'].startswith('application/json')
    data = response.get_json()
    assert 'error' in data or 'message' in data

def test_post_cart_nonexistent_product_id(client):
    response = client.post('/api/cart', json={'product_id': 9999}, follow_redirects=True)
    assert response.status_code == 404
    assert response.is_json
    assert response.headers['Content-Type'].startswith('application/json')
    data = response.get_json()
    assert 'error' in data or 'message' in data

# --- DODATKOWE TESTY BRZEGOWE ---
def test_post_cart_empty_payload(client):
    # Brak JSON w ogóle
    response = client.post('/api/cart', follow_redirects=True)
    assert response.status_code == 400
    assert response.is_json
    assert response.headers['Content-Type'].startswith('application/json')
    data = response.get_json()
    assert 'error' in data or 'message' in data

def test_post_cart_multiple_products(client, app):
    # Dodaj dwa różne produkty
    with app.app_context():
        ids = [p['id'] for p in products[:2]]
        prices = [p['price'] for p in products[:2]]
    for pid in ids:
        resp = post_product_to_cart(client, pid)
        assert resp.status_code == 201
    cart_response = client.get('/api/cart')
    assert cart_response.status_code == 200
    cart = cart_response.get_json()
    items = get_cart_items(cart_response)
    found = [False, False]
    for item in items:
        prod = item.get('product', item)
        for i, pid in enumerate(ids):
            if prod['id'] == pid:
                found[i] = True
    assert all(found)
    assert cart['total'] == sum(prices)
