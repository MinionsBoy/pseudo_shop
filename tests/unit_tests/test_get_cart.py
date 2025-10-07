import pytest
from app import app, get_cart

def test_creates_new_cart_if_not_exists():
    with app.test_request_context():
        assert get_cart() == {}

def test_cart_persistence_in_session():
    with app.test_request_context():
        cart1 = get_cart()
        cart1['1'] = 2
        cart2 = get_cart()
        assert cart2['1'] == 2

def test_cart_is_unique_per_session():
    with app.test_request_context():
        cart1 = get_cart()
        cart1['1'] = 2
    with app.test_request_context():
        cart2 = get_cart()
        assert cart2 == {}
