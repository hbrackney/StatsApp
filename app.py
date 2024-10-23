"""This is the app intialization page."""

from flask import Flask, render_template, redirect, url_for, request
from waitress import serve
from dash import Dash, dcc, html, dash_table
from dash.dependencies import Input, Output
import plotly.graph_objs as go
import pandas as pd
from scipy import stats
from statsmodels.stats.weightstats import ztest

# Intialize Flask App
app = Flask(__name__)

# Home Page Dropdown Menu Options
options = {
    "t-test": "ttest",
    "z-test": "z_test_page",
    "Example": "example_page"
}

# Interactive Charts/Graphs using Dash
"""Instructions 
Layout of the Dash app -> Each Page with a plot needs it's own set:
Dash app name
Dash app layout
Dash app callback
Update plot function"""

# Test Graph
dash_test_app = Dash(__name__, server=app, routes_pathname_prefix="/dash_test/")
dash_test_app.layout = html.Div(
    [
        html.H1("Interactive Dataset"),
        dcc.Input(id="data-input", type="number", value=1, step=1),
        dcc.Graph(id="plot"),
    ]
)


@dash_test_app.callback(Output("plot", "figure"), Input("data-input", "value"))
def update_plot_test(value):
    """Updating the plot in the interactive page

    Args:
        value (float or int): user input (defaults to 1)

    Returns: Plot the figure on the webpage
    """
    x = ["x", "x^2", "x^3"]
    y = [value, value**2, value**3]

    figure = {
        "data": [go.Bar(x=x, y=y)],
        "layout": {
            "title": "Dataset Visualization",
            "xaxis": {"title": "Functions"},
            "yaxis": {"title": "Values"},
        },
    }
    return figure


# T test plot
dash_ttest_app = Dash(__name__, server=app, routes_pathname_prefix="/dash_ttest/")

# Initial data for two datasets
initial_data1 = {
    'X Values': [1, 2, 3, 4, 5],
    'T Values': [10, 15, 13, 17, 19]
}

initial_data2 = {
    'X Values': [1, 2, 3, 4, 5],
    'T Values': [12, 14, 11, 20, 18]
}
# Convert to DataFrames for easy handling
tdf1 = pd.DataFrame(initial_data1)
tdf2 = pd.DataFrame(initial_data2)

# Layout of the Dash app
dash_ttest_app.layout = html.Div([
    html.H1("Compare Two Datasets and Calculate T-Test"),
    html.H3("Dataset 1"),
    dash_table.DataTable(
        id='data-table1',
        columns=[
            {'name': 'X Values', 'id': 'X Values', 'editable': True},
            {'name': 'T Values', 'id': 'T Values', 'editable': True},
        ],
        data=tdf1.to_dict('records'),
        editable=True,
        row_deletable=False,
        style_table={'overflowX': 'auto'},
    ),

    html.H3("Dataset 2"),
    dash_table.DataTable(
        id='data-table2',
        columns=[
            {'name': 'X Values', 'id': 'X Values', 'editable': True},
            {'name': 'T Values', 'id': 'T Values', 'editable': True},
        ],
        data=tdf2.to_dict('records'),
        editable=True,
        row_deletable=False,
        style_table={'overflowX': 'auto'},
    ),

    dcc.Graph(id='line-chart'),
    html.H3("T-Test Result"),
    html.Div(id='t-test-result')
])

# Callback to update the line chart and calculate t-test based on both tables' values
@dash_ttest_app.callback(
    Output('line-chart', 'figure'),
    Output('t-test-result', 'children'),
    Input('data-table1', 'data'),
    Input('data-table2', 'data')
)
def update_ttest_plot(data1, data2):
    """The function updates the plot and t test value
    when the user change the data."""
    data_frame1 = pd.DataFrame(data1)
    data_frame2 = pd.DataFrame(data2)

    # Perform t-test
    t_stat, p_value = stats.ttest_ind(data_frame1['T Values'],
                                      data_frame2['T Values'],
                                      nan_policy='omit')

    figure = {
        'data': [
            go.Scatter(
                x=data_frame1['X Values'],
                y=data_frame1['T Values'],
                mode='lines+markers',
                name='Dataset 1'
            ),
            go.Scatter(
                x=data_frame2['X Values'],
                y=data_frame2['T Values'],
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

    # Format t-test result
    t_test_result_text = f"T-Statistic: {t_stat:.2f}, P-Value: {p_value:.4f}"

    return figure, t_test_result_text


# Z Test Plot
dash_app = Dash(__name__, server=app, routes_pathname_prefix='/dash_ztest/')

# Initial data for two datasets
zinitial_data1 = {
    'X Values': [1, 2, 3, 4, 5],
    'Z Values': [10, 15, 13, 17, 19]
}

zinitial_data2 = {
    'X Values': [1, 2, 3, 4, 5],
    'Z Values': [12, 14, 11, 20, 18]
}

# Convert to DataFrames for easy handling
zdf1 = pd.DataFrame(zinitial_data1)
zdf2 = pd.DataFrame(zinitial_data2)

# Layout of the Dash app
dash_app.layout = html.Div([
    html.H1("Compare Two Datasets and Calculate Z-Test"),

    html.H3("Dataset 1"),
    dash_table.DataTable(
        id='data-table1',
        columns=[
            {'name': 'X Values', 'id': 'X Values', 'editable': True},
            {'name': 'Z Values', 'id': 'Z Values', 'editable': True},
        ],
        data=zdf1.to_dict('records'),
        editable=True,
        row_deletable=False,
        style_table={'overflowX': 'auto'},
    ),

    html.H3("Dataset 2"),
    dash_table.DataTable(
        id='data-table2',
        columns=[
            {'name': 'X Values', 'id': 'X Values', 'editable': True},
            {'name': 'Z Values', 'id': 'Z Values', 'editable': True},
        ],
        data=zdf2.to_dict('records'),
        editable=True,
        row_deletable=False,
        style_table={'overflowX': 'auto'},
    ),

    dcc.Graph(id='line-chart'),
    html.H3("Z-Test Result"),
    html.Div(id='z-test-result')
])

# Callback to update the line chart and calculate z-test based on both tables' values
@dash_app.callback(
    Output('line-chart', 'figure'),
    Output('z-test-result', 'children'),
    Input('data-table1', 'data'),
    Input('data-table2', 'data')
)
def update_ztest_plot(data1, data2):
    """The function updates the plot and t test value
    when the user change the data."""
    data_frame1 = pd.DataFrame(data1)
    data_frame2 = pd.DataFrame(data2)

    # Perform z-test
    z_stat, p_value = ztest(data_frame1['Z Values'],
                            data_frame2['Z Values'],
                            alternative='two-sided')

    figure = {
        'data': [
            go.Scatter(
                x=zdf1['X Values'],
                y=zdf1['Z Values'],
                mode='lines+markers',
                name='Dataset 1'
            ),
            go.Scatter(
                x=zdf2['X Values'],
                y=zdf2['Z Values'],
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

    # Format z-test result
    z_test_result_text = f"Z-Statistic: {z_stat:.2f}, P-Value: {p_value:.4f}"

    return figure, z_test_result_text

# App Routes
@app.route("/")  # Home Page
def home():
    """This function renders the home page.

    Returns: Creates the home page
    """
    return render_template("home.html", options=options)


@app.route("/submit", methods=["POST"])  # Submitting Dropdown menu Option
def submit():
    """This function submits the drop
    down box entry and take you to the home page.

    Returns: redirects to  home page
    """
    selected_option = request.form.get("options")
    if selected_option in options:
        return redirect(url_for(options[selected_option]))
    return redirect(url_for("home"))


@app.route("/ttest")
def ttest():
    """This function renders the t test page.

    Returns: Creates the t test page
    """
    return render_template("ttest.html")


@app.route("/z_test_page")
def z_test_page():
    """This function renders the z test page.

    Returns: Creates the z test page
    """
    return render_template("z_test_page.html")


@app.route("/example_page")
def example_page():
    """This function renders the interactive test
    page.

    Returns: Creates the interactive page
    """
    return render_template("example_page.html")


# @app.route("/interactive_table")
# def interactive_table():
#     """This function renders the interactive
#     table test page.

#     Returns: Creates the interactive table page
#     """
#     return render_template("interactive_table.html")

if __name__ == "__main__":
    serve(app, host="0.0.0.0", port=3000)
