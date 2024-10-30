"""This module formats the plots so they can viewed
on the app page. It holds the data and information
about the plots."""

import pandas as pd
from scipy import stats
from statsmodels.stats.weightstats import ztest
import plotly.graph_objs as go

def initialize_zero_data(rows=30):
    """Initialize data for both sample populations with zeros."""
    initial_data = {'X Values': list(range(1, rows + 1)), 'Z Values': [0] * rows}
    return pd.DataFrame(initial_data), pd.DataFrame(initial_data)

def generate_ttest_data():
    """This function creates the data for the
    t-test plot. 

    Returns:
        Dataframes: two pandas dataframes of data
    """
    # Initial data for two datasets
    initial_data1 = {
        'X Values': [1, 2, 3, 4, 5],
        'Y Values': [10, 15, 13, 17, 19]
    }
    initial_data2 = {
        'X Values': [1, 2, 3, 4, 5],
        'Y Values': [12, 14, 11, 20, 18]
    }
    return pd.DataFrame(initial_data1), pd.DataFrame(initial_data2)

def generate_ttest_plot(data1, data2):
    """This function generates the t-test plot.

    Args:
        data1 (list): two by many list
        data2 (list): two by many list

    Returns: the figure and a printed statment about
    the t-test and p value so the dash app can print them
    """
    data_frame1 = pd.DataFrame(data1)
    data_frame2 = pd.DataFrame(data2)

    # Perform t-test
    t_stat, p_value = stats.ttest_ind(data_frame1['Y Values'],
                                      data_frame2['Y Values'],
                                      nan_policy='omit')

    figure = {
        'data': [
            go.Scatter(
                x=data_frame1['X Values'],
                y=data_frame1['Y Values'],
                mode='lines+markers',
                name='Dataset 1'
            ),
            go.Scatter(
                x=data_frame2['X Values'],
                y=data_frame2['Y Values'],
                mode='lines+markers',
                name='Dataset 2'
            )
        ],
        'layout': {
            'title': 'Comparison of Two Datasets',
            'xaxis': {'title': 'X Values'},
            'yaxis': {'title': 'Y Values'},
        }
    }

    t_test_result_text = f"T-Statistic: {t_stat:.2f}, P-Value: {p_value:.4f}"
    return figure, t_test_result_text

def generate_ztest_plot(data1, data2):
    """Generates a box plot for the z-test comparing means of two sample populations."""
    data_frame1 = pd.DataFrame(data1)
    data_frame2 = pd.DataFrame(data2)

    # Convert to numeric and fill NaNs with 0
    data_frame1['Z Values'] = pd.to_numeric(data_frame1['Z Values'], errors='coerce').fillna(0)
    data_frame2['Z Values'] = pd.to_numeric(data_frame2['Z Values'], errors='coerce').fillna(0)

    # Handle cases where both columns are zeros or contain insufficient variance
    if data_frame1['Z Values'].nunique() <= 1 or data_frame2['Z Values'].nunique() <= 1:
        z_stat, p_value = float('nan'), float('nan')
        z_test_result_text = "Z-Statistic: Undefined (insufficient variance in data)"
    else:
        # Perform z-test on the input data
        z_stat, p_value = ztest(data_frame1['Z Values'], data_frame2['Z Values'], alternative='two-sided')
        z_test_result_text = f"Z-Statistic: {z_stat:.2f}, P-Value: {p_value:.4f}"

    # Create a box plot for visualization
    figure = go.Figure()
    figure.add_trace(go.Box(y=data_frame1['Z Values'], name='Population 1'))
    figure.add_trace(go.Box(y=data_frame2['Z Values'], name='Population 2'))
    figure.update_layout(
        title='Box Plot of Sample Populations',
        yaxis={'title': 'Values'}
    )
    return figure, z_test_result_text