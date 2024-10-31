"""This modules tests the plots module."""

import pytest
import pandas as pd
import plots

def test_generate_ttest_data():
    """Test the generation of t-test data."""
    data1, data2 = plots.generate_ttest_data()

    # Check that the dataframes have the correct shapes
    assert isinstance(data1, pd.DataFrame)
    assert isinstance(data2, pd.DataFrame)
    assert data1.shape == (5, 2)
    assert data2.shape == (5, 2)

    # Check that the 'Y Values' are as expected
    expected_y1 = [10, 15, 13, 17, 19]
    expected_y2 = [12, 14, 11, 20, 18]
    assert data1['Y Values'].tolist() == expected_y1
    assert data2['Y Values'].tolist() == expected_y2

def test_generate_ttest_plot():
    """Test the generation of the t-test plot."""
    data1, data2 = plots.generate_ttest_data()
    figure, t_test_result_text = plots.generate_ttest_plot(data1, data2)

    # Check that the figure contains data
    assert 'data' in figure
    assert len(figure['data']) == 2

    # Check that the layout is correct
    assert 'layout' in figure
    assert figure['layout']['title'] == 'Comparison of Two Datasets'

    # Check the result text format
    assert 'T-Statistic:' in t_test_result_text
    assert 'P-Value:' in t_test_result_text

def test_generate_ztest_plot():
    """Test the generation of the z-test plot."""
    data1, data2 = plots.initialize_random_data()
    figure, _ = plots.generate_ztest_plot(data1, data2)

    # Check that the figure contains data
    assert 'data' in figure
    assert len(figure['data']) == 2

    # Check that the layout is correct
    assert 'layout' in figure
