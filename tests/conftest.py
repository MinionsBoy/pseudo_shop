import sys
import os
import pytest
from app import app as flask_app

sys.path.insert(0, os.path.abspath(os.path.dirname(os.path.dirname(__file__))))

@pytest.fixture
def app():
    yield flask_app

@pytest.fixture
def client(app):
    return app.test_client()
