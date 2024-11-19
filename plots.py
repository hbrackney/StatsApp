"""This module formats the plots so they can viewed
on the app page. It holds the data and information
about the plots."""

import pandas as pd
from scipy import stats
from statsmodels.stats.weightstats import ztest
import plotly.graph_objs as go
import numpy as np

# T-test Table/Plot Information
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
    """
    Generates a line plot comparing two datasets and calculates 
    the t-test statistic for the difference in their means.

    Args:
        - data1 (list of dict): Data for the first dataset, where 
            each dictionary represents a row with 'X Values' and 
            'Y Values' keys.
        - data2 (list of dict): Data for the second dataset, where
            each dictionary represents a row with 'X Values' and 
            'Y Values' keys.

    Returns:
        - dict: A Plotly figure dictionary containing a line plot 
            of 'Y Values' vs. 'X Values' for both datasets.
        - str: A formatted string displaying the calculated t-test 
            statistic and p-value for the difference between the 
            two datasets.

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

# Z-test Table/Plot Information
def initialize_random_data(rows=30):
    """
    Generates random data for two sample populations 
    with values between 80 and 100.

    Args:
        - rows (int): The number of data points (rows)  
            to generate for each population.
            Defaults to 30.

    Returns:
        - pd.DataFrame: DataFrame for Population 1 
            with columns 'X Values' (index from 1 to `rows`) 
            and 'Population 1' (random values between 80 and 100).
        - pd.DataFrame: DataFrame for Population 2 
            with columns 'X Values' (index from 1 to `rows`) 
            and 'Population 2' (random values between 80 and 100).
    """
    # Generate random data between 80 and 100
    data1 = {'X Values': list(range(1, rows + 1)), 'Population 1': np.random.randint(80, 101, rows)}
    data2 = {'X Values': list(range(1, rows + 1)), 'Population 2': np.random.randint(80, 101, rows)}
    return pd.DataFrame(data1), pd.DataFrame(data2)

def generate_ztest_plot(data1, data2):
    """
    Generates a box plot and calculates the z-test statistic for comparing 
    the means of two sample populations.

    Args:
        - data1 (list of dict): Data for the first population, where each 
                                dictionary represents a row with keys such as 
                                'X Values' and 'Population 1'.
        - data2 (list of dict): Data for the second population, where each 
                                dictionary represents a row with keys such as 
                                'X Values' and 'Population 2'.

    Returns:
        - plotly.graph_objs.Figure: A box plot comparing the distributions 
            of Population 1 and Population 2.
        - str: A formatted string displaying the calculated z-test statistic 
            and p-value. If variance is insufficient, returns a message 
            indicating the z-test could not be performed.
    """
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

# Distriubtion Table/Plot Information
def generate_distribution_data():
    """This function creates the data for the
    distribution plot. 

    Returns:
        Dataframes: one pandas dataframes of data
    """
    initial_data1 = {
        'Values': list(np.linspace(1,20,20)),
    }
    return pd.DataFrame(initial_data1)

def generate_distribution_plot(data1):
    """
    Generates a dataset for creating a distribution plot.

    Returns:
        pd.DataFrame: A DataFrame containing a single column 
        'Values' with 20 evenly spaced values from 1 to 20.
    """
    data_frame1 = pd.DataFrame(data1)
    if not all(isinstance(x, (int, float)) for x in data_frame1['Values']):
        raise ValueError("All values in 'Values' must be numeric.")
    figure = {
        'data': [
            go.Histogram(
                    x=data_frame1['Values'],
                    name="Histogram"
                ),
        ],
        'layout': {
            'title': 'Histogram of Data',
            'xaxis': {'title': 'Values'},
            'yaxis': {'title': 'Frequency'},
        }
    }

    return figure
