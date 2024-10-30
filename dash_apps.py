"""This module initalizes the plots so they can be
viewed in the web app. It uses dash to do so."""

from dash import Dash, dcc, html, dash_table
from dash.dependencies import Input, Output, State
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
    zdf1, zdf2 = plots.initialize_zero_data(30)

    dash_ztest_app.layout = html.Div([
        html.H1("Compare Two Datasets and Calculate Z-Statistic Value"),
        html.Div([
            html.H3("Enter Data for Population 1"),
            create_data_table('data-table1', zdf1, 'Population 1'),
            html.Button("Add Row to Population 1", id="add-row-btn1", n_clicks=0),
        ]),
        html.Div([
            html.H3("Enter Data for Population 2"),
            create_data_table('data-table2', zdf2, 'Population 2'),
            html.Button("Add Row to Population 2", id="add-row-btn2", n_clicks=0),
        ]),
        html.Button("Update Box Plot and Z-Statistic", id="update-plot-btn", n_clicks=0),
        dcc.Graph(id='box-plot'),
        html.H3("Z-Statistic Result"),
        html.Div(id='z-test-result')
    ])

    @dash_ztest_app.callback(
        Output('data-table1', 'data'),
        Input('add-row-btn1', 'n_clicks'),
        State('data-table1', 'data')
    )
    def add_row_population1(n_clicks, data1):
        if n_clicks > 0:
            data1.append({'X Values': len(data1) + 1, 'Z Values': 0})
        return data1

    @dash_ztest_app.callback(
        Output('data-table2', 'data'),
        Input('add-row-btn2', 'n_clicks'),
        State('data-table2', 'data')
    )
    def add_row_population2(n_clicks, data2):
        if n_clicks > 0:
            data2.append({'X Values': len(data2) + 1, 'Z Values': 0})
        return data2

    @dash_ztest_app.callback(
        Output('box-plot', 'figure'),
        Output('z-test-result', 'children'),
        Input('update-plot-btn', 'n_clicks'),
        State('data-table1', 'data'),
        State('data-table2', 'data')
    )

    def update_ztest_plot(n_clicks, data1, data2):
        print("update button clicked:", n_clicks) # Debug statement
        if n_clicks > 0:
            # Convert data to numeric, ignoring non-numeric values
            data_frame1 = pd.DataFrame(data1).apply(pd.to_numeric, errors='coerce').fillna(0)
            data_frame2 = pd.DataFrame(data2).apply(pd.to_numeric, errors='coerce').fillna(0)
            
             # Check data values before proceeding (debugging)
            print("Data Frame 1:\n", data_frame1)
            print("Data Frame 2:\n", data_frame2)

            figure, z_test_result_text = plots.generate_ztest_plot(data_frame1.to_dict('records'), 
                                                                   data_frame2.to_dict('records'))
            return figure, z_test_result_text
        return go.Figure(), "No update requested."

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
