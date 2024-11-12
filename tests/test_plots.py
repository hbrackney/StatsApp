"""This modules tests the plots module."""

import pytest
import pandas as pd
import numpy as np
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

class TestGenerateDistributionData:
    """This class holds the tests for the
    generate_distribution_data function in the plots module. 
    """

    def test_generate_distribution_data(self):
        """Positive test for generate_distribution_data"""
        result = plots.generate_distribution_data()

        # Check if the result is a DataFrame
        assert isinstance(result, pd.DataFrame), "Result should be a pandas DataFrame"

        # Check if the DataFrame contains a column 'Values'
        assert 'Values' in result.columns, "'Values' column should be present in the DataFrame"

        # Check if the column 'Values' contains 20 values (from 1 to 20)
        assert len(result['Values']) == 20, "'Values' column should have 20 values"

        # Check if the values are correctly spaced from 1 to 20
        np.testing.assert_array_equal(result['Values'].values, np.linspace(1, 20, 20))

    def test_generate_distribution_data_invalid_column(self):
        """Negative test for generate_distribution_data"""
        result = plots.generate_distribution_data()

        # Check if 'Values' column contains only numeric data (float64)
        assert pd.api.types.is_numeric_dtype(result['Values']), "'Values' col must contain num data"



class TestGenerateDistributionPlot:
    """This class holds the tests for the
    generate_distribution_plot function in the plots module. 
    """

    def test_generate_distribution_plot_valid_data(self):
        """Positive test for generate_distribution_plot"""
        valid_data = {'Values': list(np.linspace(1, 20, 20))}

        figure = plots.generate_distribution_plot(valid_data)

        # Check if the figure contains the expected structure
        assert 'data' in figure, "'data' key should be present in the returned figure"
        assert 'layout' in figure, "'layout' key should be present in the returned figure"

        # Check if the 'data' part contains a histogram
        assert len(figure['data']) == 1, "'data' should contain only one histogram"
        assert figure['data'][0]['type'] == 'histogram', "'data' should contain a histogram"

        # Check if the layout contains the expected titles
        assert figure['layout']['title'] == 'Histogram of Data', "Title must be 'Histogram of Data'"
        assert figure['layout']['xaxis']['title'] == 'Values', "X-axis title should be 'Values'"
        assert figure['layout']['yaxis']['title'] == 'Frequency', "Y-axis title must be 'Frequency'"

    def test_generate_distribution_plot_invalid_data_type(self):
        """Negative test for generate_distribution_plot with invalid data"""
        invalid_data = {'Values': ['a', 'b', 'c', 'd', 'e']}

        # Test the function with invalid input (should raise ValueError or similar)
        with pytest.raises(ValueError):
            plots.generate_distribution_plot(invalid_data)

    def test_generate_distribution_plot_empty_data(self):
        """Negative test for generate_distribution_plot with empty data"""
        empty_data = {'Values': []}

        result = plots.generate_distribution_plot(empty_data)

        # Check if the result is still a valid figure, but empty histogram
        assert 'data' in result, "'data' key should be present in the returned figure"
        assert len(result['data'][0]['x']) == 0, "'data' histogram should have no values"

    def test_generate_distribution_plot_missing_values_column(self):
        """Negative test for generate_distribution_plot with missing 'Values' column"""
        missing_column_data = {'SomeOtherColumn': [1, 2, 3, 4, 5]}

        # Test the function with invalid input (missing 'Values' column)
        with pytest.raises(KeyError):
            plots.generate_distribution_plot(missing_column_data)
