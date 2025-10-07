import pytest
from app import products
from tests.utils.api_helpers import assert_product_fields

def test_get_product_details_existing(client, app):
    with app.app_context():
        existing_id = 2
        expected = next((p for p in products if p['id'] == existing_id), None)
        required_fields = {"id", "name", "price", "description"}

    response = client.get(f"/api/products/{existing_id}", follow_redirects=True)
    assert response.status_code == 200
    assert response.is_json
    assert response.headers['Content-Type'].startswith('application/json')
    data = response.get_json()
    assert isinstance(data, dict)
    assert_product_fields(data)
    assert data["id"] == existing_id
    assert data["name"] == expected["name"]
    assert data["price"] == expected["price"]
    assert data["description"] == expected["description"]


def test_get_product_details_not_found(client):
    non_existing_id = 9999
    response = client.get(f"/api/products/{non_existing_id}", follow_redirects=True)
    assert response.status_code == 404
    assert response.is_json
    assert response.headers['Content-Type'].startswith('application/json')
    data = response.get_json()
    assert "error" in data or "message" in data  # Accept either key for error info

# --- DODATKOWE TESTY BRZEGOWE ---
def test_get_product_details_invalid_id(client):
    # Nieprawidłowy identyfikator (string zamiast int)
    response = client.get("/api/products/abc", follow_redirects=True)
    # Flask powinien zwrócić 404 (niepoprawny URL)
    assert response.status_code == 404

def test_get_product_details_min_id(client, app):
    # Najmniejszy możliwy id
    with app.app_context():
        min_id = min(p['id'] for p in products)
        expected = next((p for p in products if p['id'] == min_id), None)
    response = client.get(f"/api/products/{min_id}", follow_redirects=True)
    assert response.status_code == 200
    data = response.get_json()
    assert data['id'] == min_id
    assert data['name'] == expected['name']
