"""This modules tests the plots module."""

import pytest
import pandas as pd
import numpy as np
import plotly.graph_objs as go
import plots

class TestGenerateTTestData:
    """Tests for the generate_ttest_data function."""

    def test_generate_ttest_data(self):
        """Test that the generate_ttest_data function returns two correct DataFrames."""
        data1, data2 = plots.generate_ttest_data()

        # Check if the return values are dataframes
        assert isinstance(data1, pd.DataFrame)
        assert isinstance(data2, pd.DataFrame)

        # Check if they have the correct columns
        assert list(data1.columns) == ['X Values', 'Y Values']
        assert list(data2.columns) == ['X Values', 'Y Values']

        # Check the data in the first dataframe
        assert data1['X Values'].tolist() == [1, 2, 3, 4, 5]
        assert data1['Y Values'].tolist() == [10, 15, 13, 17, 19]

        # Check the data in the second dataframe
        assert data2['X Values'].tolist() == [1, 2, 3, 4, 5]
        assert data2['Y Values'].tolist() == [12, 14, 11, 20, 18]


class TestGenerateTTestPlot:
    """Tests for the generate_ttest_plot function."""

    def test_generate_ttest_plot_valid_data(self):
        """Test generate_ttest_plot with valid data."""
        data1 = {'X Values': [1, 2, 3, 4, 5], 'Y Values': [10, 15, 13, 17, 19]}
        data2 = {'X Values': [1, 2, 3, 4, 5], 'Y Values': [12, 14, 11, 20, 18]}

        figure, t_test_result_text = plots.generate_ttest_plot(data1, data2)

        # Test that the return values are correct types
        assert isinstance(figure, dict)  # A plotly figure dictionary
        assert 'data' in figure  # Check if the 'data' key exists in the figure

        # Check for specific t-statistics and p-values
        assert "T-Statistic:" in t_test_result_text
        assert "P-Value:" in t_test_result_text

    def test_generate_ttest_plot_empty_data(self):
        """Test with empty data."""
        data1 = {'X Values': [], 'Y Values': []}
        data2 = {'X Values': [], 'Y Values': []}

        figure, t_test_result_text = plots.generate_ttest_plot(data1, data2)

        # The result should still produce a plot figure, but the t-test should handle empty data
        assert isinstance(figure, dict)
        assert 'data' in figure
        assert 'layout' in figure

        # Check if the t-test string is well-formatted even for empty data
        assert t_test_result_text == "T-Statistic: nan, P-Value: nan"

    def test_generate_ttest_plot_data_with_nans(self):
        """Test with data containing NaN values."""
        data1 = {'X Values': [1, 2, 3, 4, 5], 'Y Values': [10, 15, None, 17, 19]}
        data2 = {'X Values': [1, 2, 3, 4, 5], 'Y Values': [12, 14, 11, None, 18]}

        figure, t_test_result_text = plots.generate_ttest_plot(data1, data2)

        # Check if the function handles NaN values gracefully
        assert isinstance(figure, dict)
        assert 'data' in figure
        assert 'layout' in figure

        # Check if the t-test result text is well-formatted
        assert isinstance(t_test_result_text, str)
        assert "T-Statistic:" in t_test_result_text
        assert "P-Value:" in t_test_result_text

    def test_generate_ttest_plot_different_lengths(self):
        """Test with data of different lengths."""
        data1 = {'X Values': [1, 2, 3, 4, 5], 'Y Values': [10, 15, 13, 17, 19]}
        data2 = {'X Values': [1, 2, 3], 'Y Values': [12, 14, 11]}

        figure, t_test_result_text = plots.generate_ttest_plot(data1, data2)

        # Ensure the function handles different lengths correctly
        assert isinstance(figure, dict)
        assert 'data' in figure
        assert len(figure['data']) == 2  # Expecting two datasets to be plotted
        assert "T-Statistic:" in t_test_result_text
        assert "P-Value:" in t_test_result_text

class TestInitializeRandomData:
    """Tests for the initialize_random_data function."""

    def test_initialize_random_data_default(self):
        """Test that initialize_random_data returns two dataframes with default rows (30)."""
        data1, data2 = plots.initialize_random_data()

        # Check if the return values are dataframes
        assert isinstance(data1, pd.DataFrame)
        assert isinstance(data2, pd.DataFrame)

        # Check if the dataframes have 30 rows
        assert len(data1) == 30
        assert len(data2) == 30

        # Check if the dataframes have the correct columns
        assert list(data1.columns) == ['X Values', 'Population 1']
        assert list(data2.columns) == ['X Values', 'Population 2']

        # Check that the values are within the expected range (80 to 100)
        assert data1['Population 1'].between(80, 100).all()
        assert data2['Population 2'].between(80, 100).all()

    def test_initialize_random_data_custom_rows(self):
        """Test with custom row count."""
        data1, data2 = plots.initialize_random_data(rows=50)

        # Check if the dataframes have 50 rows
        assert len(data1) == 50
        assert len(data2) == 50

    def test_initialize_random_data_zero_rows(self):
        """Test with zero rows (should return empty dataframes)."""
        data1, data2 = plots.initialize_random_data(rows=0)

        # Check if the dataframes are empty
        assert len(data1) == 0
        assert len(data2) == 0

        # Ensure the columns are still present
        assert list(data1.columns) == ['X Values', 'Population 1']
        assert list(data2.columns) == ['X Values', 'Population 2']


class TestGenerateZTestPlot:
    """Tests for the generate_ztest_plot function."""

    def test_generate_ztest_plot_valid_data(self):
        """Test generate_ztest_plot with valid data."""
        data1 = {'X Values': [1, 2, 3, 4, 5], 'Population 1': [90, 92, 88, 95, 91]}
        data2 = {'X Values': [1, 2, 3, 4, 5], 'Population 2': [80, 85, 87, 84, 82]}

        figure, z_test_result_text = plots.generate_ztest_plot(data1, data2)

        # Test that the return values are correct types
        assert isinstance(figure, go.Figure)  # A plotly figure object
        assert 'data' in figure.to_dict()  # Check if the 'data' key exists in the figure

        # Check if the z-test result text is correctly formatted
        assert isinstance(z_test_result_text, str)
        assert z_test_result_text.startswith("Z-Statistic:")
        assert "P-value:" in z_test_result_text

    def test_generate_ztest_plot_insufficient_variance(self):
        """Test with data where one of the populations has insufficient variance."""
        data1 = {'X Values': [1, 2, 3, 4, 5], 'Population 1': [90, 90, 90, 90, 90]}
        data2 = {'X Values': [1, 2, 3, 4, 5], 'Population 2': [85, 85, 85, 85, 85]}

        figure, z_test_result_text = plots.generate_ztest_plot(data1, data2)

        # Check if the function handles insufficient variance
        assert isinstance(figure, go.Figure)
        assert 'data' in figure.to_dict()
        assert "Z-Statistic: Undefined" in z_test_result_text

    def test_generate_ztest_plot_with_zeros(self):
        """Test with data where both populations have all zero values."""
        data1 = {'X Values': [1, 2, 3, 4, 5], 'Population 1': [0, 0, 0, 0, 0]}
        data2 = {'X Values': [1, 2, 3, 4, 5], 'Population 2': [0, 0, 0, 0, 0]}

        figure, z_test_result_text = plots.generate_ztest_plot(data1, data2)

        # Check if the function handles zero variance gracefully
        assert isinstance(figure, go.Figure)
        assert 'data' in figure.to_dict()
        assert "Z-Statistic: Undefined" in z_test_result_text

    def test_generate_ztest_plot_empty_data(self):
        """Test with empty data."""
        data1 = {'X Values': [], 'Population 1': []}
        data2 = {'X Values': [], 'Population 2': []}

        figure, z_test_result_text = plots.generate_ztest_plot(data1, data2)

        # The result should still produce a plot figure, but the z-test should handle empty data
        assert isinstance(figure, go.Figure)
        assert 'data' in figure.to_dict()
        assert "Z-Statistic: Undefined" in z_test_result_text

    def test_generate_ztest_plot_different_lengths(self):
        """Test with data of different lengths."""
        data1 = {'X Values': [1, 2, 3, 4, 5], 'Population 1': [90, 92, 88, 95, 91]}
        data2 = {'X Values': [1, 2, 3], 'Population 2': [80, 85, 87]}

        # Check if the function gracefully handles different lengths (may need to truncate or align)
        figure, z_test_result_text = plots.generate_ztest_plot(data1, data2)

        assert isinstance(figure, go.Figure)
        assert 'data' in figure.to_dict()
        assert "Z-Statistic:" in z_test_result_text
        assert "P-value:" in z_test_result_text


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
