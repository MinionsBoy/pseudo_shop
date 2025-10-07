import pytest
from app import products
from tests.utils.api_helpers import assert_product_fields

def test_get_products(client, app):
    # Arrange: get the products list from the app context if possible
    with app.app_context():
        expected_count = len(products)
        required_fields = {"id", "name", "price", "description"}

    # Act
    response = client.get('/api/products', follow_redirects=True)

    # Assert
    assert response.status_code == 200
    assert response.is_json
    assert response.headers['Content-Type'].startswith('application/json')
    data = response.get_json()
    assert isinstance(data, list)
    assert len(data) == expected_count
    for product in data:
        assert_product_fields(product)

# --- DODATKOWE TESTY BRZEGOWE ---
def test_get_products_not_empty(client):
    response = client.get('/api/products', follow_redirects=True)
    data = response.get_json()
    assert isinstance(data, list)
    assert len(data) > 0

def test_get_products_fields_types(client):
    response = client.get('/api/products', follow_redirects=True)
    data = response.get_json()
    for product in data:
        assert_product_fields(product)

def test_get_products_content_type(client):
    response = client.get('/api/products', follow_redirects=True)
    assert response.headers['Content-Type'].startswith('application/json')