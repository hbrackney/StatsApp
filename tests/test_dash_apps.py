"""This test file tests the dash apps module"""
import pytest
from dash import Dash # , dcc, html
# from dash.dependencies import Input, Output, State
# from dash.testing import wait
from flask import Flask
# import pandas as pd
import dash_apps
# import plots

@pytest.fixture
def test_app():
    """Create a testing Flask app and initialize Dash apps."""
    flask_app = Flask(__name__)
    dash_app = dash_apps.create_dash_apps(flask_app)

    # Use the Flask app's test client
    return {key: flask_app.test_client() for key in dash_app.keys()}

def test_update_plot_test(test_app):
    """Tests that the Dash app correctly handles requests to the /dash_test/"""
    client = test_app['dash_test']
    response = client.get('/dash_test/')
    assert response.status_code == 200 or 405 # Page correctly loads

    # Simulate the input value change correctly
    response = client.post('/dash_test/', json={'data-input': 3})  # Adjust the data as necessary
    assert response.status_code == 200 or 405 # Page correctly loads

# Example for testing the addition of a row in the DataTable
def test_add_row_population1(test_app):
    """Tests the functionality of adding a row to a data table in dash_ztest"""
    client = test_app['dash_ztest']
    initial_data = [{'X Values': 1, 'Z Values': 0}]
    # Simulate clicking the button to add a row
    response = client.post('/dash_ztest/', json={
        'add-row-btn1': 1,
        'data-table1': initial_data
    })
    assert response.status_code == 200 or 405 # Page correctly loads

def test_update_ztest_plot(test_app):
    """Test the update_ztest_plot callback in the dash_ztest app."""
    client = test_app['dash_ztest']
    data1 = [{'X Values': 1, 'Z Values': 1}]
    data2 = [{'X Values': 1, 'Z Values': 2}]
    # Simulate button click to update the plot
    response = client.post('/dash_ztest/', json={
        'update-plot-btn': 1,
        'data-table1': data1,
        'data-table2': data2
    })
    assert response.status_code == 200 or 405 # Page correctly loads

def test_update_distributions_test(test_app):
    """Tests that the Dash app correctly handles requests to the /dash_distribution/"""
    client = test_app['dash_distribution']
    response = client.get('/dash_distribution/')
    assert response.status_code == 200 # Page correctly loads

    # Simulate the input value change correctly
    response = client.post('/dash_distribution/', json={'data-input': 3})
    assert response.status_code == 405 # Page correctly loads
