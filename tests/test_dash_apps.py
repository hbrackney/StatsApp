"""This module tests the dash_apps"""
import pytest
from dash import html, dcc
# import pandas as pd
from flask import Flask
from app import create_dash_apps


@pytest.fixture
def test_app():
    """This function creates the testing app."""
    # Create a basic Dash app instance
    flask_app = Flask(__name__)
    return create_dash_apps(flask_app)

def test_dash_test_app_layout(test_app):
    """This function tests that the layout
    is formatting correctly.
    
    Args:
        app (flash_app): testing app"""
    dash_test_app = test_app['dash_test']

    # Check if the layout contains expected elements
    assert isinstance(dash_test_app.layout, html.Div)
    assert any(child.children == 'Interactive Dataset' for child in dash_test_app.layout.children)
    assert isinstance(dash_test_app.layout.children[1], dcc.Input)
    assert isinstance(dash_test_app.layout.children[2], dcc.Graph)

def test_update_plot_test(test_app):
    """This function tests that plots
    update correctly.
    
    Args:
        app (flash_app): testing app"""
    dash_test_app = test_app['dash_test']

    # Simulate user input
    input_value = 3
    expected_y = [input_value, input_value**2, input_value**3]

    # Call the callback function directly
    figure = dash_test_app.callback_map['plot']['update_plot_test'](input_value)

    # Check if the figure data is correct
    assert len(figure['data']) == 1
    assert figure['data'][0]['y'] == expected_y

def test_add_row_population1(test_app):
    """This function tests if a row is
    added correctly.
    
    Args:
        app (flash_app): testing app"""
    ztest_app = test_app['dash_ztest']

    # Set initial data directly
    initial_data = [{'X Values': 1, 'Z Values': 0}]
    ztest_app.layout.children[1].data = initial_data  # Assign initial data

    # Simulate adding a row
    updated_data = ztest_app.callback_map['data-table1']['add_row_population1'](1, initial_data)

    # Check if a new row has been added
    assert len(updated_data) == 2
    assert updated_data[-1] == {'X Values': 2, 'Z Values': 0}

def test_update_ztest_plot(test_app):
    """This function test that the ztest
    plot is updating correctly. 

    Args:
        app (flash_app): testing app
    """
    ztest_app = test_app['dash_ztest']

    # Prepare input data
    data1 = [{'X Values': 1, 'Z Values': 1}]
    data2 = [{'X Values': 1, 'Z Values': 2}]

    # Call the update callback directly
    figure, z_test_result = ztest_app.callback_map['box-plot']['update_ztest_plot'](1, data1, data2)

    # Check if the figure is returned correctly
    assert isinstance(figure, dict)  # Check that figure is a dictionary
    assert 'Z-Statistic Result' in z_test_result  # Check if result contains expected text
