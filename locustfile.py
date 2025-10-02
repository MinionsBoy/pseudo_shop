"""
Locust performance testing script for the pseudo shop application.

This file defines user behaviour for load testing using Locust.  Each
simulated user will repeatedly browse the list of products and then
view a specific product and add it to the cart via the JSON API.  You
can run the load test by executing ``locust`` in the project root and
opening the web UI at ``http://localhost:8089``.  For headless runs
see the Locust documentation.

See the official quick start guide for more details on Locust usage【287612495241309†L45-L74】.
"""
from random import choice
from locust import HttpUser, task, between

# List of product IDs.  Keeping this list in the test file avoids having
# to import application code inside the load test runner.  Adjust if you
# add or remove products in ``app.py``.
PRODUCT_IDS = [1, 2, 3, 4]


class ShopUser(HttpUser):
    # Wait between 1 and 3 seconds between tasks to simulate human pacing
    wait_time = between(1, 3)

    @task(2)
    def browse_products(self):
        """Retrieve the list of products via the API."""
        self.client.get('/api/products')

    @task(1)
    def view_and_add_product(self):
        """View a random product and add it to the cart via the API."""
        pid = choice(PRODUCT_IDS)
        self.client.get(f'/api/products/{pid}')
        # Add to cart.  POSTing JSON is required by the API.
        self.client.post('/api/cart', json={'product_id': pid})