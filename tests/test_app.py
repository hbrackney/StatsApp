"""This module tests that the app loads correctly.
The tests check that the pages exist."""

import pytest
from app import app

@pytest.fixture
def client():
    """Create a test client for the Flask application."""
    app.config['TESTING'] = True
    with app.test_client() as test_client:
        yield test_client

def test_home_page(client):
    """Test that the home page loads successfully."""
    response = client.get('/')
    assert response.status_code == 200
    assert b'Welcome!' in response.data

def test_about_page(client):
    """Test that the about page loads successfully."""
    response = client.get('/about')
    assert response.status_code == 200
    assert b'About' in response.data

def test_ttest_page(client):
    """Test that the t-test page loads successfully."""
    response = client.get('/ttest')
    assert response.status_code == 200
    assert b't-test' in response.data

def test_ztest_page(client):
    """Test that the z-test page loads successfully."""
    response = client.get('/z_test_page')
    assert response.status_code == 200
    assert b'z-test' in response.data

def test_distribution_page(client):
    """Test that the z-test page loads successfully."""
    response = client.get('/distributions_page')
    assert response.status_code == 200
    assert b'distribution' in response.data

def test_reference_page(client):
    """Test that the example page loads successfully."""
    response = client.get('/reference_page')
    assert response.status_code == 200
    assert b'concept' in response.data
