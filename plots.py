"""This module formats the plots so they can viewed
on the app page. It holds the data and information
about the plots."""

import pandas as pd
from scipy import stats
from statsmodels.stats.weightstats import ztest
import plotly.graph_objs as go


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

def generate_ztest_data():
    """This function creates the data for the
    z-test plot. 

    Returns:
        Dataframes: two pandas dataframes of data
    """
    # Initial data for two datasets
    zinitial_data1 = {
        'X Values': [1, 2, 3, 4, 5],
        'Y Values': [10, 15, 13, 17, 19]
    }
    zinitial_data2 = {
        'X Values': [1, 2, 3, 4, 5],
        'Y Values': [12, 14, 11, 20, 18]
    }
    return pd.DataFrame(zinitial_data1), pd.DataFrame(zinitial_data2)

def generate_ztest_plot(data1, data2):
    """This function generates the z-test plot.

    Args:
        data1 (list): two by many list
        data2 (list): two by many list

    Returns: the figure and a printed statment about
    the z-test and p value so the dash app can print them
    """
    data_frame1 = pd.DataFrame(data1)
    data_frame2 = pd.DataFrame(data2)

    # Perform z-test
    z_stat, p_value = ztest(data_frame1['Y Values'],
                            data_frame2['Y Values'],
                            alternative='two-sided')

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

    z_test_result_text = f"Z-Statistic: {z_stat:.2f}, P-Value: {p_value:.4f}"
    return figure, z_test_result_text
