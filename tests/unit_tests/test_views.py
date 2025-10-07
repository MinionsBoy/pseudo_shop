import pytest
from app import app, products


def test_index_view(client):
    response = client.get('/')
    assert response.status_code == 200
    for prod in products:
        assert prod['name'] in response.get_data(as_text=True)

def test_product_detail_view_existing(client):
    prod = products[0]
    response = client.get(f'/product/{prod["id"]}')
    assert response.status_code == 200
    assert prod['name'] in response.get_data(as_text=True)

def test_product_detail_view_404(client):
    response = client.get('/product/9999')
    assert response.status_code == 404

def test_cart_view_empty(client):
    response = client.get('/cart')
    assert response.status_code == 200
    assert "Koszyk" in response.get_data(as_text=True)

def test_cart_view_with_product(client):
    prod = products[0]
    client.post(f'/add_to_cart/{prod["id"]}', follow_redirects=True)
    response = client.get('/cart')
    assert response.status_code == 200
    page = response.get_data(as_text=True)
    assert prod['name'] in page
    assert "Koszyk" in page
