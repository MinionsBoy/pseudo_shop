import pytest
from app import get_product_by_id, calculate_cart_total, products

def test_empty_product_list(monkeypatch):
    monkeypatch.setattr('app.products', [])
    assert get_product_by_id(1) is None

def test_large_numbers_in_cart():
    cart = {str(products[0]['id']): 10**6}
    total = calculate_cart_total(cart)
    assert total == products[0]['price'] * 10**6

def test_input_not_modified():
    cart = {'1': 2}
    cart_copy = cart.copy()
    calculate_cart_total(cart)
    assert cart == cart_copy
