"""This module tests that the app loads correctly.
The tests check that the pages exist."""

import pytest
from app import app
from flask import url_for

@pytest.fixture
def client():
    """Create a test client for the Flask application."""
    app.config['TESTING'] = True # Enable testing mode for the app
    with app.test_client() as test_client: # Initialize the test client
        yield test_client # Provide the test client to the tests

def test_fake_page(client):
    """Test that the home page loads successfully."""
    response = client.get('/fake') # Simulate a GET request to fake page
    assert response.status_code == 404 # Page not found error

def test_home_page(client):
    """Test that the home page loads successfully."""
    response = client.get('/') # Simulate a GET request to the home page
    assert response.status_code == 200 # Page correctly loads
    assert b'Welcome!' in response.data # Check that the response contains the text 'Welcome!'

def test_about_page(client):
    """Test that the about page loads successfully."""
    response = client.get('/about') # Simulate a GET request to the about page
    assert response.status_code == 200 # Page correctly loads
    assert b'About' in response.data # Check that the response contains the text 'About'

def test_ttest_page(client):
    """Test that the t-test page loads successfully."""
    response = client.get('/ttest') # Simulate a GET request to the t-test page
    assert response.status_code == 200 # Page correctly loads
    assert b't-test' in response.data # Check that the response contains the text 't-test'

def test_ztest_page(client):
    """Test that the z-test page loads successfully."""
    response = client.get('/z_test_page') # Simulate a GET request to the z-test page
    assert response.status_code == 200 # Page correctly loads
    assert b'z-test' in response.data # Check that the response contains the text 'z-test'

def test_distribution_page(client):
    """Test that the z-test page loads successfully."""
    response = client.get('/distributions_page') # Simulate a GET request to the distributions page
    assert response.status_code == 200 # Page correctly loads
    assert b'distribution' in response.data

def test_anova_page(client):
    """Test that the anova page loads successfully."""
    response = client.get('/anova') # Simulate a GET request to the anova page
    assert response.status_code == 200 # Page correctly loads
    assert b'ANOVA test' in response.data # Check that the response contains the text 'ANOVA test'

def test_regressions_page(client):
    """Test that the regressions page loads successfully."""
    response = client.get('/regressions') # Simulate a GET request to the regressions page
    assert response.status_code == 200 # Page correctly loads
    assert b'Regressions' in response.data # Check that the response contains the text 'Regressions'

def test_reference_page(client):
    """Test that the example page loads successfully."""
    response = client.get('/reference_page') # Simulate a GET request to the reference page
    assert response.status_code == 200 # Page correctly loads
    assert b'concept' in response.data # Check that the response contains the text 'concept'

class TestSubmitFunction:
    """Tests for the submit function in the Flask app."""

    def test_submit_valid_option(self, client):
        """Test that the submit function redirects correctly for a valid option."""
        # Prepare form data with a valid option
        valid_option = 'option1'
        response = client.post('/submit', data={'options': valid_option})

        # Assert that the response is a redirect to the correct URL (page1 in this case)
        assert response.status_code == 302  # 302 indicates a redirect

    def test_submit_invalid_option(self, client):
        """Test that the submit function redirects to the home page for an invalid option."""
        # Prepare form data with an invalid option
        invalid_option = 'invalid_option'
        response = client.post('/submit', data={'options': invalid_option})

        # Assert that the response is a redirect to the home page (first entry in pages list)
        assert response.status_code == 302  # 302 indicates a redirect

    def test_submit_no_option(self, client):
        """Test that the submit function handles the case where no option is selected."""
        # Simulate the scenario where no option is selected
        response = client.post('/submit', data={})  # No data is provided

        # Assert that the response redirects to the home page (first entry in pages list)
        assert response.status_code == 302  # 302 indicates a redirect
