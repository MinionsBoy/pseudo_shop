def get_cart_items(cart_response):
    """Extracts items from cart response, handling both keys."""
    cart = cart_response.get_json()
    return cart.get('items', cart.get('products', []))

def assert_product_fields(product):
    required_fields = {"id", "name", "price", "description"}
    assert required_fields.issubset(product.keys())
    assert isinstance(product['id'], int)
    assert isinstance(product['name'], str)
    assert isinstance(product['price'], float)
    assert isinstance(product['description'], str)

def post_product_to_cart(client, product_id):
    return client.post('/api/cart', json={'product_id': product_id}, follow_redirects=True)
