"""This modules tests the plots module."""

import pytest
import pandas as pd
import numpy as np
import plotly.graph_objs as go
import plots

class TestGenerateTTestData:
    """Tests for the generate_ttest_data function."""

    def test_initialize_ttest_data(self):
        """Test that the initialize_ttest_data function returns two correct DataFrames."""
        data1, data2 = plots.initialize_ttest_data(rows=10)

        # Check if the return values are dataframes
        assert isinstance(data1, pd.DataFrame), "First output should be a DataFrame"
        assert isinstance(data2, pd.DataFrame), "Second output should be a DataFrame"

        # Check if they have the correct columns
        assert list(data1.columns) == ['X Values', 'Population 1'], "DataFrame 1 should have 'X Values' and 'Population 1'"
        assert list(data2.columns) == ['X Values', 'Population 2'], "DataFrame 2 should have 'X Values' and 'Population 2'"

        # Check the length of the DataFrames
        assert len(data1) == 10, "DataFrame 1 should have 10 rows"
        assert len(data2) == 10, "DataFrame 2 should have 10 rows"

        # Check the values in the DataFrames
        assert data1['X Values'].tolist() == list(range(1, 11)), "X Values in DataFrame 1 should be consecutive numbers from 1 to 10"
        assert data2['X Values'].tolist() == list(range(1, 11)), "X Values in DataFrame 2 should be consecutive numbers from 1 to 10"

        # Verify that Population 1 and Population 2 values are within the expected range
        assert data1['Population 1'].between(80, 100).all(), "Population 1 values should be between 80 and 100"
        assert data2['Population 2'].between(80, 100).all(), "Population 2 values should be between 80 and 100"


class TestGenerateTTestPlot:
    """Tests for the generate_ttest_plot function."""

    def test_generate_ttest_plot_valid_data(self):
        """Test generate_ttest_plot with valid data."""
        data1 = [{'X Values': 1, 'Population 1': 10},
                 {'X Values': 2, 'Population 1': 15},
                 {'X Values': 3, 'Population 1': 13},
                 {'X Values': 4, 'Population 1': 17},
                 {'X Values': 5, 'Population 1': 19}]
        data2 = [{'X Values': 1, 'Population 2': 12},
                 {'X Values': 2, 'Population 2': 14},
                 {'X Values': 3, 'Population 2': 11},
                 {'X Values': 4, 'Population 2': 20},
                 {'X Values': 5, 'Population 2': 18}]

        figure, t_test_result_text = plots.generate_ttest_plot(data1, data2)

        # Test that the return values are correct types
        assert isinstance(figure, go.Figure), "Output should be a Plotly Figure"
        assert "T-Statistic:" in t_test_result_text
        assert "P-Value:" in t_test_result_text

    def test_generate_ttest_plot_empty_data(self):
        """Test with empty data."""
        data1 = {'X Values': [], 'Population 1': []}
        data2 = {'X Values': [], 'Population 2': []}

        figure, t_test_result_text = plots.generate_ttest_plot(data1, data2)

        # Ensure the result is a valid figure and handles empty data gracefully
        assert isinstance(figure, go.Figure), "Output should be a Plotly Figure"
        assert 'data' in figure.to_dict(), "Figure should have a 'data' key"
        assert "T-Test: Insufficient data for calculation." == t_test_result_text

    def test_generate_ttest_plot_data_with_nans(self):
        """Test with data containing NaN values."""
        data1 = [{'X Values': 1, 'Population 1': 10},
                 {'X Values': 2, 'Population 1': 15},
                 {'X Values': 3, 'Population 1': None},
                 {'X Values': 4, 'Population 1': 17},
                 {'X Values': 5, 'Population 1': 19}]
        data2 = [{'X Values': 1, 'Population 2': 12},
                 {'X Values': 2, 'Population 2': 14},
                 {'X Values': 3, 'Population 2': 11},
                 {'X Values': 4, 'Population 2': None},
                 {'X Values': 5, 'Population 2': 18}]

        figure, t_test_result_text = plots.generate_ttest_plot(data1, data2)

        # Ensure the function handles NaN values gracefully
        assert isinstance(figure, go.Figure), "Output should be a Plotly Figure"
        assert len(figure.data) == 2, "Figure should plot two datasets"
        assert "T-Statistic:" in t_test_result_text
        assert "P-Value:" in t_test_result_text

    def test_generate_ttest_plot_different_lengths(self):
        """Test with data of different lengths."""
        data1 = [{'X Values': 1, 'Population 1': 10},
                 {'X Values': 2, 'Population 1': 15},
                 {'X Values': 3, 'Population 1': 13},
                 {'X Values': 4, 'Population 1': 17},
                 {'X Values': 5, 'Population 1': 19}]
        data2 = [{'X Values': 1, 'Population 2': 12},
                 {'X Values': 2, 'Population 2': 14},
                 {'X Values': 3, 'Population 2': 11}]

        figure, t_test_result_text = plots.generate_ttest_plot(data1, data2)

        # Ensure the function handles different lengths gracefully
        assert isinstance(figure, go.Figure), "Output should be a Plotly Figure"
        assert len(figure.data) == 2, "Figure should plot two datasets"
        assert "T-Statistic:" in t_test_result_text
        assert "P-Value:" in t_test_result_text

    def test_generate_ttest_plot_insufficient_sample_size(self):
        """Test with insufficient sample size for t-test."""
        data1 = [{'X Values': 1, 'Population 1': 10}]
        data2 = [{'X Values': 1, 'Population 2': 12}]

        figure, t_test_result_text = plots.generate_ttest_plot(data1, data2)

        # Ensure the function handles insufficient data gracefully
        assert isinstance(figure, go.Figure), "Output should be a Plotly Figure"
        assert len(figure.data) == 0, "Figure should have no data for insufficient input"
        assert t_test_result_text == "T-Test: Insufficient data for calculation."


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

    def test_initialize_linear_data(self):
        """Test the initialize_linear_data function."""
        rows = 5
        df = plots.initialize_linear_data(rows)

        # Verify the DataFrame structure
        assert isinstance(df, pd.DataFrame), "Output should be a pandas DataFrame"
        assert list(df.columns) == ['X Values', 'Y Values'], "DataFrame should have 'X Values' and 'Y Values' columns"

        # Verify the number of rows
        assert len(df) == rows, f"DataFrame should have {rows} rows"

        # Verify the linear relationship: Y = 2X + 1
        x_expected = np.arange(1, rows + 1)
        y_expected = 2 * x_expected + 1
        assert (df['X Values'].values == x_expected).all(), "X Values should be consecutive integers starting from 1"
        assert (df['Y Values'].values == y_expected).all(), "Y Values should follow the equation Y = 2X + 1"


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

class TestGenerateRegressionPlot:
    '''
    A test suite for the `generate_linear_regression_plot` function in the plots module.
    The function is tested for:
    - Correct calculation of the regression line equation and R² value.
    - Proper handling of edge cases, such as empty data, invalid data types, 
      missing columns, and non-numeric values.
    '''
    def test_generate_linear_regression_plot(self):
        """Test the generate_linear_regression_plot function."""
        # Input data following a perfect linear relationship
        data = [
            {'X Values': 1, 'Y Values': 3},
            {'X Values': 2, 'Y Values': 5},
            {'X Values': 3, 'Y Values': 7},
            {'X Values': 4, 'Y Values': 9}
        ]

        figure, equation, r2_value = plots.generate_linear_regression_plot(data)

        # Verify the equation is correct
        expected_equation = "y = 2.00x + 1.00"
        assert equation == expected_equation, f"Expected equation: {expected_equation}, but got: {equation}"

        # Verify the R^2 value is 1.0 (perfect fit)
        assert r2_value == 1.0, f"Expected R^2 value of 1.0, but got: {r2_value}"

        # Verify the figure contains the expected traces
        assert isinstance(figure, go.Figure), "Output figure should be a Plotly Figure"
        assert len(figure.data) == 2, "Figure should have 2 traces (data points and regression line)"
        assert figure.data[0].name == "Data Points", "First trace should represent data points"
        assert figure.data[1].name == "Regression Line", "Second trace should represent the regression line"

    def test_generate_linear_regression_plot_empty_data(self):
        """Test generate_linear_regression_plot with no data."""
        empty_data = []

        # Test the function with empty input (should raise KeyError for missing columns)
        with pytest.raises(KeyError):
            plots.generate_linear_regression_plot(empty_data)
    
    def test_generate_linear_regression_plot_invalid_data_type(self):
        """Negative test for generate_linear_regression_plot with invalid data type."""
        invalid_data = {'X Values': ['a', 'b', 'c'], 'Y Values': [1, 2, 3]}

        # Test the function with invalid input (should raise ValueError or similar)
        with pytest.raises(ValueError):
            plots.generate_linear_regression_plot(invalid_data)

    def test_generate_linear_regression_plot_missing_columns(self):
        """Negative test for generate_linear_regression_plot with missing columns."""
        missing_column_data = [{'SomeOtherColumn': [1, 2, 3]}]

        # Test the function with missing 'X Values' or 'Y Values' columns (should raise KeyError)
        with pytest.raises(KeyError):
            plots.generate_linear_regression_plot(missing_column_data)

    def test_generate_linear_regression_plot_non_numeric_values(self):
        """Test generate_linear_regression_plot with non-numeric values."""
        non_numeric_data = [
            {'X Values': 1, 'Y Values': 'a'},  # 'Y Values' contains non-numeric data
            {'X Values': 'b', 'Y Values': 2}  # 'X Values' contains non-numeric data
        ]

        # Expect the function to raise a ValueError when non-numeric data is present
        with pytest.raises(ValueError, match="Data contains no valid numeric values after cleaning"):
            plots.generate_linear_regression_plot(non_numeric_data)
