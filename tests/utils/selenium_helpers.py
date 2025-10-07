def assert_product_equal(prod1, prod2):
	assert prod1 == prod2
	assert isinstance(prod1['id'], int)
	assert isinstance(prod1['name'], str)
	assert isinstance(prod1['price'], float)
	assert isinstance(prod1['description'], str)

def make_cart(products, quantities):
	"""Return a cart dict for given products and quantities."""
	return {str(p['id']): q for p, q in zip(products, quantities)}
