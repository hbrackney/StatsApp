"""This module formats the plots so they can viewed
on the app page. It holds the data and information
about the plots."""

import pandas as pd
from scipy import stats
from statsmodels.stats.weightstats import ztest
from sklearn.linear_model import LinearRegression
from sklearn.metrics import r2_score
import plotly.graph_objs as go
import numpy as np

# T-test Table/Plot Information
def initialize_ttest_data(rows=10):
    """
    Generates random data for two sample populations with values between 80 and 100.

    Args:
        - rows (int): The number of data points to generate. Defaults to 10.

    Returns:
        - pd.DataFrame: DataFrame for Population 1 with randomized values.
        - pd.DataFrame: DataFrame for Population 2 with randomized values.
    """
    data1 = {'X Values': list(range(1, rows + 1)), 'Population 1': np.random.randint(80, 101, rows)}
    data2 = {'X Values': list(range(1, rows + 1)), 'Population 2': np.random.randint(80, 101, rows)}
    return pd.DataFrame(data1), pd.DataFrame(data2)

# T-test Table/Plot Information
def initialize_ttest_data(rows=10):
    """
    Generates random data for two sample populations with values between 80 and 100.

    Args:
        - rows (int): The number of data points to generate. Defaults to 10.

    Returns:
        - pd.DataFrame: DataFrame for Population 1 with randomized values.
        - pd.DataFrame: DataFrame for Population 2 with randomized values.
    """
    data1 = {'X Values': list(range(1, rows + 1)), 'Population 1': np.random.randint(80, 101, rows)}
    data2 = {'X Values': list(range(1, rows + 1)), 'Population 2': np.random.randint(80, 101, rows)}
    return pd.DataFrame(data1), pd.DataFrame(data2)

def generate_ttest_plot(data1, data2):
    """
    Generates a box plot and calculates the t-test statistic for comparing
    the means of two sample populations.

    Args:
        - data1 (list of dict): Data for Population 1, with keys such as 'X Values' and 'Population 1'.
        - data2 (list of dict): Data for Population 2, with keys such as 'X Values' and 'Population 2'.

    Returns:
        - plotly.graph_objs.Figure: A box plot comparing the distributions of Population 1 and Population 2.
        - str: A formatted string displaying the t-test statistic and p-value.
    """
    df1 = pd.DataFrame(data1)
    df2 = pd.DataFrame(data2)

    # Extract numeric values for t-test calculations
    values1 = pd.to_numeric(df1['Population 1'], errors='coerce').dropna()
    values2 = pd.to_numeric(df2['Population 2'], errors='coerce').dropna()

    # Handle insufficient sample sizes
    if len(values1) < 2 or len(values2) < 2:
        return go.Figure(), "T-Test: Insufficient data for calculation."

    # Perform t-test
    t_stat, p_value = stats.ttest_ind(values1, values2, equal_var=False, nan_policy='omit')

    # Create a box plot
    figure = go.Figure()
    figure.add_trace(go.Box(y=values1, name='Population 1'))
    figure.add_trace(go.Box(y=values2, name='Population 2'))
    figure.update_layout(
        title="Box Plot of Sample Populations",
        yaxis={"title": "Values"}
    )

    # Format t-test results for display
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

    # Extract numeric values for z-test calculations
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
    # Initialize sequence of 20 evenly spaced numbers between 1 and 20
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
    # Check that all elements in 'Values' column are numeric and raise error if not
    if not all(isinstance(x, (int, float)) for x in data_frame1['Values']):
        raise ValueError("All values in 'Values' must be numeric.")
    
    # Create a histogram for visualization
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

def initialize_anova_data(rows=30):
    """
    Generates random data for three sample populations 
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
        - pd.DataFrame: DataFrame for Population 3 
            with columns 'X Values' (index from 1 to `rows`) 
            and 'Population 3' (random values between 80 and 100).
    """
    # Generate random data between 80 and 100 for three populations
    data1 = {'X Values': list(range(1, rows + 1)), 'Population 1': np.random.randint(80, 101, rows)}
    data2 = {'X Values': list(range(1, rows + 1)), 'Population 2': np.random.randint(80, 101, rows)}
    data3 = {'X Values': list(range(1, rows + 1)), 'Population 3': np.random.randint(80, 101, rows)}
    return pd.DataFrame(data1), pd.DataFrame(data2), pd.DataFrame(data3)

def generate_anova_plot(data1, data2, data3):
    """
    Generates a box plot and calculates the ANOVA test statistic for comparing 
    the means of three sample populations.

    Args:
        - data1 (list of dict): Data for the first population, where each 
                                dictionary represents a row with keys such as 
                                'X Values' and 'Population 1'.
        - data2 (list of dict): Data for the second population, where each 
                                dictionary represents a row with keys such as 
                                'X Values' and 'Population 2'.
        - data3 (list of dict): Data for the third population, where each 
                                dictionary represents a row with keys such as 
                                'X Values' and 'Population 3'.

    Returns:
        - plotly.graph_objs.Figure: A box plot comparing the distributions 
            of Population 1, Population 2, and Population 3.
        - str: A formatted string displaying the calculated ANOVA F-statistic 
            and p-value.
    """
    data_frame1 = pd.DataFrame(data1)
    data_frame2 = pd.DataFrame(data2)
    data_frame3 = pd.DataFrame(data3)

    # Extract numeric values for ANOVA calculations
    if 'Population 1' in data_frame1.columns and 'Population 2' in data_frame2.columns and 'Population 3' in data_frame3.columns:
        values1 = pd.to_numeric(data_frame1['Population 1'], errors='coerce').fillna(0)
        values2 = pd.to_numeric(data_frame2['Population 2'], errors='coerce').fillna(0)
        values3 = pd.to_numeric(data_frame3['Population 3'], errors='coerce').fillna(0)
    else:
        # Fallback if columns are named differently
        values1 = data_frame1['Z Values']
        values2 = data_frame2['Z Values']
        values3 = data_frame3['Z Values']

    # Perform one-way ANOVA
    f_stat, p_value = stats.f_oneway(values1, values2, values3)

    # Create a box plot for visualization
    figure = go.Figure()
    figure.add_trace(go.Box(y=values1, name='Population 1', marker=dict(color='blue')))
    figure.add_trace(go.Box(y=values2, name='Population 2', marker=dict(color='green')))
    figure.add_trace(go.Box(y=values3, name='Population 3', marker=dict(color='red')))
    figure.update_layout(
        title=f"ANOVA Test: F-statistic = {f_stat:.2f}, P-value = {p_value:.4f}",
        yaxis={'title': 'Values'},
        xaxis={'title': 'Groups'},
        showlegend=False
    )

    # Provide explanation based on p-value
    if p_value < 0.05:
        anova_result_text = f"ANOVA Test: F-statistic = {f_stat:.2f}, P-value = {p_value:.4f}\nThe p-value is less than 0.05, indicating that there is a significant difference between the groups."
    else:
        anova_result_text = f"ANOVA Test: F-statistic = {f_stat:.2f}, P-value = {p_value:.4f}\nThe p-value is greater than 0.05, indicating that there is no significant difference between the groups."

    return figure, anova_result_text

# Initialize data table for Regressions page
def initialize_linear_data(rows=10):
    """
    Generates initial data for linear regression with X values starting at 1 
    and increasing by 2, and Y values calculated as 2X + 1.

    Args:
        rows (int): Number of rows to generate. Defaults to 10.

    Returns:
        pd.DataFrame: A DataFrame with 'X Values' and 'Y Values' columns.
    """
    x_values = np.arange(1, rows + 1)  # Generate consecutive integers starting from 1
    y_values = 2 * x_values + 1 # Initial values should follow a linear regresion model for plotting purposes
    return pd.DataFrame({"X Values": x_values, "Y Values": y_values})

# Generate interactive plot for Regressions page
def generate_linear_regression_plot(data):
    """
    Generates a scatter plot with a linear regression line based on input data.

    Args:
        data (list of dict): Data for the regression, where each dictionary 
                             represents a row with 'X Values' and 'Y Values' keys.

    Returns:
        - plotly.graph_objs.Figure: A scatter plot with a regression line.
        - str: The linear regression equation in the format y = mx + b.
        - float: The R^2 value indicating the goodness of fit.

    Raises:
        KeyError: If required columns ('X Values', 'Y Values') are missing.
        ValueError: If the input data contains invalid types or inconsistent lengths.

    """
    # Check if the data is a list of dictionaries
    if not isinstance(data, list) or not all(isinstance(row, dict) for row in data):
        raise ValueError("Input data must be a list of dictionaries")

    # Convert input data to a DataFrame
    df = pd.DataFrame(data)

    # Check for required columns
    if 'X Values' not in df.columns or 'Y Values' not in df.columns:
        raise KeyError("Input data must contain 'X Values' and 'Y Values' columns")

    # Ensure columns are numeric
    df = df.apply(pd.to_numeric, errors='coerce').dropna()
    if df.empty:
        raise ValueError("Data contains no valid numeric values after cleaning")

    # Perform linear regression
    X = df['X Values'].values.reshape(-1, 1)
    Y = df['Y Values'].values
    model = LinearRegression()
    model.fit(X, Y)
    Y_pred = model.predict(X)

    # Generate regression equation
    slope = model.coef_[0]
    intercept = model.intercept_
    r2_value = r2_score(Y, Y_pred)
    equation = f"y = {slope:.2f}x + {intercept:.2f}"

    # Create scatter plot with regression line
    figure = go.Figure()
    figure.add_trace(go.Scatter(x=df['X Values'], y=df['Y Values'], mode='markers', name='Data Points'))
    figure.add_trace(go.Scatter(x=df['X Values'], y=Y_pred, mode='lines', name='Regression Line'))
    figure.update_layout(
        title="Linear Regression Plot",
        xaxis_title="X Values",
        yaxis_title="Y Values",
        showlegend=True
    )

    return figure, equation, r2_value
