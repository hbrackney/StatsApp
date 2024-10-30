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
    
    # Ensure we are using the correct columns for z-test calculations
    if 'Population 1' in data_frame1.columns and 'Population 2' in data_frame2.columns:
        values1 = pd.to_numeric(data_frame1['Population 1'], errors='coerce').fillna(0)
        values2 = pd.to_numeric(data_frame2['Population 2'], errors='coerce').fillna(0)
    else:
        # Fallback if columns are named differently
        values1 = data_frame1['Z Values']
        values2 = data_frame2['Z Values']

    # Handle cases where both columns are zeros or contain insufficient variance
    if values1.nunique() <= 1 or values2.nunique() <= 1:
        z_stat, p_value = float('nan'), float('nan')
        z_test_result_text = "Z-Statistic: Undefined (insufficient variance in data)"
    else:
        # Perform z-test on the input data
        z_stat, p_value = ztest(values1, values2, alternative='two-sided')
        z_test_result_text = f"Z-Statistic: {z_stat:.2f}, P-value: {p_value:.4f}"

    # Create a box plot for visualization
    figure = go.Figure()
    figure.add_trace(go.Box(y=values1, name='Population 1'))
    figure.add_trace(go.Box(y=values2, name='Population 2'))
    figure.update_layout(
        title='Box Plot of Sample Populations',
        yaxis={'title': 'Values'}
    )
    
    return figure, z_test_result_text