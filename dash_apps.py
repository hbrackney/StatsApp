"""This module initalizes the plots so they can be
viewed in the web app. It uses dash to do so."""

from dash import Dash, dcc, html, dash_table
from dash.dependencies import Input, Output
import plotly.graph_objs as go
import plots

def create_dash_apps(flask_app):
    """This function creates the dash app
    so the plots can be interactive and viewed
    on the web app.

    Args:
        flask_app (flash_app): This function need an
        active flask app to intialize.

    Returns:
        dictionary: The dictionary of a dictionary
        contains the information needs for the dash apps
        to start up.
    """
    # Test Graph
    dash_test_app = Dash(__name__, server=flask_app, routes_pathname_prefix="/dash_test/")
    dash_test_app.layout = html.Div(
        [
            html.H1("Interactive Dataset"),
            dcc.Input(id="data-input", type="number", value=1, step=1),
            dcc.Graph(id="plot"),
        ]
    )

    @dash_test_app.callback(Output("plot", "figure"), Input("data-input", "value"))
    def update_plot_test(value):
        """This function takes in the user
        inputted value to change the plot as needed.

        Args:
            value (int): Web app user inputted number

        Returns:
            figure: the new updated plot is outputted.
        """
        x = ["x", "x^2", "x^3"]
        y = [value, value**2, value**3]

        return {
            "data": [go.Bar(x=x, y=y)],
            "layout": {
                "title": "Dataset Visualization",
                "xaxis": {"title": "Functions"},
                "yaxis": {"title": "Values"},
            },
        }

    # T-test Plot
    dash_ttest_app = Dash(__name__, server=flask_app, routes_pathname_prefix="/dash_ttest/")
    tdf1, tdf2 = plots.generate_ttest_data()

    dash_ttest_app.layout = html.Div([
        html.H1("Compare Two Datasets and Calculate T-Test"),
        create_data_table('data-table1', tdf1, 'Y-Values'),
        create_data_table('data-table2', tdf2, 'Y-Values'),
        dcc.Graph(id='line-chart'),
        html.H3("T-Test Result"),
        html.Div(id='t-test-result')
    ])

    @dash_ttest_app.callback(
        Output('line-chart', 'figure'),
        Output('t-test-result', 'children'),
        Input('data-table1', 'data'),
        Input('data-table2', 'data')
    )
    def update_ttest_plot(data1, data2):
        """This function takes in the user
        inputted value to change the plot as needed.

        Args:
            data1: Web app user inputted numbers
            data2: Web app user inputted numbers

        Returns:
            figure: the new updated plot is outputted.
        """
        return plots.generate_ttest_plot(data1, data2)

    # Z-Test Plot
    dash_ztest_app = Dash(__name__, server=flask_app, routes_pathname_prefix='/dash_ztest/')
    zdf1, zdf2 = plots.generate_ztest_data()

    dash_ztest_app.layout = html.Div([
        html.H1("Compare Two Datasets and Calculate Z-Test"),
        create_data_table('data-table1', zdf1, 'Z Values'),
        create_data_table('data-table2', zdf2, 'Z Values'),
        dcc.Graph(id='line-chart'),
        html.H3("Z-Test Result"),
        html.Div(id='z-test-result')
    ])

    @dash_ztest_app.callback(
        Output('line-chart', 'figure'),
        Output('z-test-result', 'children'),
        Input('data-table1', 'data'),
        Input('data-table2', 'data')
    )
    def update_ztest_plot(data1, data2):
        """This function takes in the user
        inputted value to change the plot as needed.

        Args:
            data1: Web app user inputted numbers
            data2: Web app user inputted numbers

        Returns:
            figure: the new updated plot is outputted.
        """
        return plots.generate_ztest_plot(data1, data2)

def create_data_table(table_id, data, value_col):
    """This function creates the tables for the 
    user to interact with.

    Args:
        table_id (int): table identifying number 
        data (list): dataframe of information for the table
        value_col (str): name of the column

    Returns:
        dictionary: table information for the dash
        app to format
    """
    return dash_table.DataTable(
        id=table_id,
        columns=[
            {'name': 'X Values', 'id': 'X Values', 'editable': True},
            {'name': value_col, 'id': value_col, 'editable': True},
        ],
        data=data.to_dict('records'),
        editable=True,
        row_deletable=False,
        style_table={'overflowX': 'auto'},
    )