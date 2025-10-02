"""
Simple Flask pseudo-shop application.

This module defines a minimal e‑commerce style web application that allows
users to browse a list of products, view product details, add items to
their cart and remove them again.  A set of JSON API endpoints mirror
the HTML views so that automated tests can interact with the same
functionality programmatically.

The application is intentionally kept simple.  It stores product
information in memory and persists the shopping cart inside the user
session.  No database is required.  The goal is to provide a real
runnable app that can be used as a basis for writing unit tests,
Selenium tests, API tests and performance tests.

To run this application use the instructions in the accompanying
``README.md`` file.
"""

from flask import Flask, render_template, session, redirect, url_for, request, jsonify, flash

app = Flask(__name__)
# Secret key is required for session management.  In a real application
# you should generate a strong random key and keep it secret.
app.config['SECRET_KEY'] = 'change-me-please'

# In‑memory list of products.  Each product has an id, name,
# description and price.  In a production application this data would
# reside in a database.
products = [
    {
        'id': 1,
        'name': 'Piłka nożna',
        'description': 'Profesjonalna piłka do gry w piłkę nożną o rozmiarze 5.',
        'price': 99.99,
    },
    {
        'id': 2,
        'name': 'Rękawice bramkarskie',
        'description': 'Wygodne rękawice bramkarskie z doskonałą przyczepnością.',
        'price': 79.50,
    },
    {
        'id': 3,
        'name': 'Koszulka sportowa',
        'description': 'Przewiewna koszulka sportowa wykonana z technicznego materiału.',
        'price': 59.00,
    },
    {
        'id': 4,
        'name': 'Buty biegowe',
        'description': 'Lekki i wygodny model obuwia przeznaczony do biegania.',
        'price': 199.99,
    },
]


def get_product_by_id(product_id: int):
    """Return a product dict by id or ``None`` if not found."""
    for product in products:
        if product['id'] == product_id:
            return product
    return None


def get_cart():
    """Retrieve the user's cart from the session.

    The cart is stored as a dictionary mapping product ids to quantities.
    If no cart exists yet, an empty dict is created and saved in the
    session.
    """
    cart = session.get('cart')
    if cart is None:
        cart = {}
        session['cart'] = cart
    return cart


def calculate_cart_total(cart: dict) -> float:
    """Calculate the total cost of items in the cart.

    :param cart: dictionary mapping product ids (as strings) to quantities
    :return: total cost as float
    """
    total = 0.0
    for pid_str, qty in cart.items():
        try:
            pid = int(pid_str)
        except (ValueError, TypeError):
            continue
        product = get_product_by_id(pid)
        if product:
            total += product['price'] * qty
    return total


@app.route('/')
def index():
    """Render the home page showing all products with optional search and sorting.

    Supported query parameters:
    - q: case-insensitive search over product name and description
    - sort: one of 'name', 'price_asc', 'price_desc'
    """
    query = (request.args.get('q') or '').strip().lower()
    sort = (request.args.get('sort') or '').strip()

    filtered = products
    if query:
        filtered = [
            p for p in products
            if query in p['name'].lower() or query in p['description'].lower()
        ]

    if sort == 'name':
        filtered = sorted(filtered, key=lambda p: p['name'].lower())
    elif sort == 'price_asc':
        filtered = sorted(filtered, key=lambda p: p['price'])
    elif sort == 'price_desc':
        filtered = sorted(filtered, key=lambda p: p['price'], reverse=True)

    return render_template('index.html', products=filtered, q=query, sort=sort)


@app.route('/product/<int:product_id>')
def product_detail(product_id: int):
    """Render details for a single product.

    If the product does not exist a 404 page is returned.
    """
    product = get_product_by_id(product_id)
    if product is None:
        return render_template('404.html'), 404
    return render_template('product_detail.html', product=product)


@app.route('/add_to_cart/<int:product_id>', methods=['POST', 'GET'])
def add_to_cart(product_id: int):
    """Add a product to the shopping cart.

    If the product doesn't exist, redirect back to home.  On success the
    user is redirected to the cart page.
    """
    product = get_product_by_id(product_id)
    if not product:
        return redirect(url_for('index'))
    cart = get_cart()
    # Flask stores session values as serialisable types, so we use string keys.
    pid_str = str(product_id)
    cart[pid_str] = cart.get(pid_str, 0) + 1
    session['cart'] = cart
    flash('Dodano produkt do koszyka')
    return redirect(url_for('cart'))


@app.route('/remove_from_cart/<int:product_id>', methods=['POST', 'GET'])
def remove_from_cart(product_id: int):
    """Remove a product from the shopping cart.

    Decrements the quantity; if quantity reaches zero the product is removed
    entirely.  After updating the cart the user is redirected back to the
    cart page.
    """
    cart = get_cart()
    pid_str = str(product_id)
    if pid_str in cart:
        if cart[pid_str] > 1:
            cart[pid_str] -= 1
        else:
            del cart[pid_str]
        session['cart'] = cart
    flash('Zaktualizowano koszyk')
    return redirect(url_for('cart'))


@app.route('/increase_qty/<int:product_id>', methods=['POST'])
def increase_qty(product_id: int):
    cart = get_cart()
    pid_str = str(product_id)
    if pid_str in cart:
        cart[pid_str] += 1
        session['cart'] = cart
        flash('Zwiększono ilość')
    return redirect(url_for('cart'))


@app.route('/decrease_qty/<int:product_id>', methods=['POST'])
def decrease_qty(product_id: int):
    cart = get_cart()
    pid_str = str(product_id)
    if pid_str in cart:
        if cart[pid_str] > 1:
            cart[pid_str] -= 1
        else:
            del cart[pid_str]
        session['cart'] = cart
        flash('Zmniejszono ilość')
    return redirect(url_for('cart'))


@app.route('/clear_cart', methods=['POST'])
def clear_cart():
    session['cart'] = {}
    flash('Wyczyszczono koszyk')
    return redirect(url_for('cart'))


@app.route('/cart')
def cart():
    """Render the cart page showing items and total cost."""
    cart = get_cart()
    items = []
    for pid_str, qty in cart.items():
        pid = int(pid_str)
        product = get_product_by_id(pid)
        if product:
            items.append({'product': product, 'quantity': qty})
    total = calculate_cart_total(cart)
    return render_template('cart.html', items=items, total=total)


# -----------------------------------------------------------------------------
# API Endpoints
#
# These routes expose the same functionality of the HTML views as a JSON API.
# They are useful for automated API testing and for performance tests using
# tools like Locust.  The endpoints follow REST‑like conventions.
# -----------------------------------------------------------------------------


@app.route('/api/products')
def api_get_products():
    """Return a JSON list of all products."""
    return jsonify(products)


@app.route('/api/products/<int:product_id>')
def api_get_product(product_id: int):
    """Return details for a single product in JSON format.

    Returns a 404 status code if the product does not exist.
    """
    product = get_product_by_id(product_id)
    if product is None:
        return jsonify({'error': 'product not found'}), 404
    return jsonify(product)


@app.route('/api/cart', methods=['GET'])
def api_get_cart():
    """Return the current cart as JSON."""
    cart = get_cart()
    # Build a response that includes product details and quantities
    response_items = []
    for pid_str, qty in cart.items():
        pid = int(pid_str)
        product = get_product_by_id(pid)
        if product:
            response_items.append({'product': product, 'quantity': qty})
    return jsonify({'items': response_items, 'total': calculate_cart_total(cart)})


@app.route('/api/cart', methods=['POST'])
def api_add_to_cart():
    """Add a product to the cart via JSON request.

    The POST body should contain JSON with a 'product_id' field.  If the
    product exists it is added to the cart and a success response is
    returned.  Otherwise a 404 response is returned.
    """
    data = request.get_json(silent=True) or {}
    product_id = data.get('product_id')
    if not isinstance(product_id, int):
        return jsonify({'error': 'invalid product_id'}), 400
    product = get_product_by_id(product_id)
    if not product:
        return jsonify({'error': 'product not found'}), 404
    cart = get_cart()
    pid_str = str(product_id)
    cart[pid_str] = cart.get(pid_str, 0) + 1
    session['cart'] = cart
    return jsonify({'message': 'product added to cart'}), 201


@app.context_processor
def inject_cart_count():
    """Provide cart_count to all templates (sum of quantities)."""
    cart = session.get('cart') or {}
    try:
        count = sum(int(qty) for qty in cart.values())
    except Exception:
        count = 0
    return {'cart_count': count}


if __name__ == '__main__':
    # Running the Flask development server directly via ``python app.py``
    # enables easier debugging.  In production use a proper WSGI server.
    app.run(debug=True)