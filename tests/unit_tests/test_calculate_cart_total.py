import pytest
from app import calculate_cart_total, products
from tests.utils.selenium_helpers import make_cart
from app import products

def test_single_product_total():
    cart = make_cart([products[0]], [2])
    expected = products[0]['price'] * 2
    assert calculate_cart_total(cart) == expected

def test_multiple_products_total():
    cart = make_cart(products[:2], [1, 3])
    expected = products[0]['price'] * 1 + products[1]['price'] * 3
    assert calculate_cart_total(cart) == expected

def test_empty_cart_total():
    assert calculate_cart_total({}) == 0

def test_zero_and_negative_price():
    prod = {'id': 99, 'name': 'Free', 'description': 'Zero', 'price': 0.0}
    prod_neg = {'id': 100, 'name': 'Refund', 'description': 'Negative', 'price': -10.0}
    products.extend([prod, prod_neg])
    cart = {'99': 5}
    cart_neg = {'100': 2}
    assert calculate_cart_total(cart) == 0
    assert calculate_cart_total(cart_neg) == -20.0
    # Clean up
    products.remove(prod)
    products.remove(prod_neg)
