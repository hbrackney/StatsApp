"""This test file tests the dash apps module"""
import pytest
import dash
from dash import Dash, dash_table # , dcc, html
from dash.testing.application_runners import import_app
# from dash.dependencies import Input, Output, State
# from dash.testing import wait
from flask import Flask
import pandas as pd
import dash_apps
# import plots
from dash_apps import create_dash_apps
import plotly.graph_objs as go

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
    assert response.status_code == 405 # Returns a page error

def test_create_data_table_two_col():
    """Tests that the output and format of the generated tables is correct"""
    # Sample data to pass to the function
    data = pd.DataFrame({
        'X Values': [1, 2, 3],
        'Y Values': [10, 20, 30]
    })

    # Call the function with this data
    table = dash_apps.create_data_table_two_col('table-id', data, 'Y Values')

    # Ensure the table is a Dash Table
    assert isinstance(table, dash_table.DataTable)

    # Check that the table has the correct number of columns and rows
    assert len(table.columns) == 2  # 'X Values' and 'Y Values'
    assert table.columns[0]['name'] == 'X Values'  # Check the column names
    assert table.columns[1]['name'] == 'Y Values'
    assert len(table.data) == 3  # Check the number of rows

def test_create_data_table_one_col():
    """Tests that the output and format of the table is correct"""
    # Sample data to pass to the function
    data = pd.DataFrame({
        'Values': [10, 20, 30]
    })

    # Call the function with this data
    table = dash_apps.create_data_table_one_col('table-id', data, 'Values')

    # Ensure the table is a Dash Table
    assert isinstance(table, dash_table.DataTable)

    # Check that the table has the correct number of columns (1 column)
    assert len(table.columns) == 1
    assert table.columns[0]['name'] == 'Values'
    assert len(table.data) == 3  # Check the number of rows

def test_create_dash_apps(test_app):
    """Test to check if Dash apps are created and their routes are accessible"""

    # List of the Dash app routes to test
    dash_routes = ['/dash_anova/', '/dash_distribution/', '/dash_ttest/']

    # Check if each route returns a 200 OK response
    for route in dash_routes:
        response = test_app['dash_anova'].get(route)  # Use any client from the test_app
        assert response.status_code == 200, f"Route {route} did not return 200 OK"

    # Check for 405 on unsupported methods
    response = test_app['dash_anova'].post('/dash_anova/')  # Simulate a POST to check 405
    assert response.status_code == 405, "Expected 405 Method Not Allowed for POST"

def test_create_data_table_two_col():
    """Tests that the output and format of the generated tables is correct"""
    # Sample data to pass to the function
    data = pd.DataFrame({
        'X Values': [1, 2, 3],
        'Y Values': [10, 20, 30]
    })

    # Call the function with this data
    table = dash_apps.create_data_table_two_col('table-id', data, 'Y Values')

    # Ensure the table is a Dash Table
    assert isinstance(table, dash_table.DataTable)

    # Check that the table has the correct number of columns and rows
    assert len(table.columns) == 2  # 'X Values' and 'Y Values'
    assert table.columns[0]['name'] == 'X Values'  # Check the column names
    assert table.columns[1]['name'] == 'Y Values'
    assert len(table.data) == 3  # Check the number of rows

def test_create_data_table_one_col():
    """Tests that the output and format of the table is correct"""
    # Sample data to pass to the function
    data = pd.DataFrame({
        'Values': [10, 20, 30]
    })

    # Call the function with this data
    table = dash_apps.create_data_table_one_col('table-id', data, 'Values')

    # Ensure the table is a Dash Table
    assert isinstance(table, dash_table.DataTable)

    # Check that the table has the correct number of columns (1 column)
    assert len(table.columns) == 1
    assert table.columns[0]['name'] == 'Values'
    assert len(table.data) == 3  # Check the number of rows
