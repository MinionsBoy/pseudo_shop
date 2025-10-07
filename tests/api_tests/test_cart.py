import pytest
from app import products
from tests.utils.api_helpers import get_cart_items, post_product_to_cart

def test_get_cart_empty(client):
    response = client.get('/api/cart', follow_redirects=True)
    assert response.status_code == 200
    assert response.is_json
    assert response.headers['Content-Type'].startswith('application/json')
    data = response.get_json()
    assert isinstance(data, dict)
    assert 'total' in data
    assert data['total'] == 0
    items = get_cart_items(response)
    assert isinstance(items, list)
    assert len(items) == 0

def test_get_cart_with_products(client, app):
    with app.app_context():
        product_id = products[0]['id']
        price = products[0]['price']
    # Add product to cart
    post_product_to_cart(client, product_id)
    post_product_to_cart(client, product_id)
    response = client.get('/api/cart', follow_redirects=True)
    assert response.status_code == 200
    assert response.is_json
    assert response.headers['Content-Type'].startswith('application/json')
    data = response.get_json()
    assert 'total' in data
    assert data['total'] == 2 * price
    items = get_cart_items(response)
    found = False
    for item in items:
        prod = item.get('product', item)
        if prod['id'] == product_id:
            assert item.get('quantity', 1) == 2
            found = True
    assert found

# --- DODATKOWE TESTY BRZEGOWE ---
def test_cart_add_and_remove(client, app):
    # Dodaj produkt, usuń go i sprawdź czy koszyk pusty
    with app.app_context():
        pid = products[0]['id']
    post_product_to_cart(client, pid)
    # Usuwanie przez endpoint HTML, ale sprawdzamy efekt w API
    client.post(f'/remove_from_cart/{pid}', follow_redirects=True)
    response = client.get('/api/cart')
    data = response.get_json()
    items = data.get('items', data.get('products', []))
    # Produkt powinien zniknąć
    for item in items:
        prod = item.get('product', item)
        assert prod['id'] != pid
    assert data['total'] == 0

def test_cart_clear(client, app):
    # Dodaj dwa produkty, wyczyść koszyk
    with app.app_context():
        ids = [p['id'] for p in products[:2]]
    for pid in ids:
        post_product_to_cart(client, pid)
    client.post('/clear_cart', follow_redirects=True)
    response = client.get('/api/cart')
    data = response.get_json()
    items = data.get('items', data.get('products', []))
    assert len(items) == 0
    assert data['total'] == 0

def test_cart_increase_decrease_qty(client, app):
    # Dodaj produkt, zwiększ i zmniejsz ilość
    with app.app_context():
        pid = products[0]['id']
        price = products[0]['price']
    post_product_to_cart(client, pid)
    client.post(f'/increase_qty/{pid}', follow_redirects=True)
    response = client.get('/api/cart')
    data = response.get_json()
    items = data.get('items', data.get('products', []))
    for item in items:
        prod = item.get('product', item)
        if prod['id'] == pid:
            assert item.get('quantity', 1) == 2
    client.post(f'/decrease_qty/{pid}', follow_redirects=True)
    response = client.get('/api/cart')
    data = response.get_json()
    items = data.get('items', data.get('products', []))
    for item in items:
        prod = item.get('product', item)
        if prod['id'] == pid:
            assert item.get('quantity', 1) == 1
