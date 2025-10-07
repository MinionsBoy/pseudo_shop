import pytest
from app import get_product_by_id, products
from tests.utils.selenium_helpers import assert_product_equal

def test_returns_product_for_existing_id():
    prod = products[0]
    result = get_product_by_id(prod['id'])
    assert_product_equal(result, prod)

def test_returns_none_for_nonexistent_id():
    assert get_product_by_id(9999) is None

@pytest.mark.parametrize("bad_id", ["abc", None, 1.5, {}, []])
def test_handles_invalid_id_type(bad_id):
    assert get_product_by_id(bad_id) is None
