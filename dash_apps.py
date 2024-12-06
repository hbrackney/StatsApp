"""This module initalizes the plots so they can be
viewed in the web app. It uses dash to do so."""

from dash import Dash, dcc, html, dash_table
from dash.dependencies import Input, Output, State
import pandas as pd
import numpy as np
import plotly.graph_objs as go
import plots

def create_dash_apps(flask_app):
    """This decorator creates the dash app
    so the plots can be interactive and viewed
    on the web app. The functions in this decorator
    change the plots as needed and ensure everything
    is formatted correctly.

    Args:
        flask_app (flash_app): This function need an
        active flask app to intialize.

    Returns:
        dictionary: The dictionary of a dictionary
        contains the information needs for the dash apps
        to start up.
    """
    # Test Graph for the Reference Page
    dash_test_app = Dash(__name__, server=flask_app, routes_pathname_prefix="/dash_test/")
    dash_test_app.layout = html.Div(
        [
            html.H1("Interactive Dataset"),
            dcc.Input(id="data-input", type="number", value=1, step=1),
            dcc.Graph(id="plot"),
        ]
    )

    @dash_test_app.callback(Output("plot", "figure"), Input("data-input", "value"))
    def update_plot_test(value: float):
        """This function generates a bar plot based on a
        user-provided input value. As the user changes
        the inputted value, the plot will change. 

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

    # Making the T-test figures
    dash_ttest_app = Dash(__name__, server=flask_app, routes_pathname_prefix="/dash_ttest/")
    tdf1, tdf2 = plots.initialize_ttest_data(10)

    # T-test Data Table
    # T-Test Data Table and Plot Layout
    dash_ttest_app.layout = html.Div([
        html.H1("Compare Two Datasets and Calculate T-Test"),
        html.Div([
            html.H3("Enter Data for Population 1"),
            create_data_table_two_col('ttest-data-table1', tdf1, 'Population 1'),
            html.Button("Add Row to Population 1", id="ttest-add-row-btn1", n_clicks=0),
        ]),
        html.Div([
            html.H3("Enter Data for Population 2"),
            create_data_table_two_col('ttest-data-table2', tdf2, 'Population 2'),
            html.Button("Add Row to Population 2", id="ttest-add-row-btn2", n_clicks=0),
        ]),
        html.Button("Update Box Plot and T-Test", id="ttest-update-plot-btn", n_clicks=0),
        dcc.Graph(id='ttest-box-plot'),
        html.H3("T-Test Result"),
        html.Div(id='ttest-result', style={'marginTop': '20px'}),
    ])

    # T-test Plot
    # Callback to add rows to Population 1
    @dash_ttest_app.callback(
        Output('ttest-data-table1', 'data'),
        Input('ttest-add-row-btn1', 'n_clicks'),
        State('ttest-data-table1', 'data')
    )
    def add_row_ttest_population1(n_clicks, data1):
        if n_clicks > 0:
            data1.append({'X Values': len(data1) + 1, 'Population 1': np.random.randint(80, 101)})
        return data1

    # Callback to add rows to Population 2
    @dash_ttest_app.callback(
        Output('ttest-data-table2', 'data'),
        Input('ttest-add-row-btn2', 'n_clicks'),
        State('ttest-data-table2', 'data')
    )
    def add_row_ttest_population2(n_clicks, data2):
        if n_clicks > 0:
            data2.append({'X Values': len(data2) + 1, 'Population 2': np.random.randint(80, 101)})
        return data2

    # Callback to update the T-Test Plot and Results
    @dash_ttest_app.callback(
        Output('ttest-box-plot', 'figure'),
        Output('ttest-result', 'children'),
        Input('ttest-update-plot-btn', 'n_clicks'),
        State('ttest-data-table1', 'data'),
        State('ttest-data-table2', 'data')
    )
    def update_ttest_plot(n_clicks, data1, data2):
        if n_clicks > 0:
            figure, t_test_result_text = plots.generate_ttest_plot(data1, data2)
            return figure, t_test_result_text
        return go.Figure(), "No updates requested."

    # Z-Test Figures
    dash_ztest_app = Dash(__name__, server=flask_app, routes_pathname_prefix='/dash_ztest/')
    zdf1, zdf2 = plots.initialize_random_data(30)

    # Z-test Data Table
    dash_ztest_app.layout = html.Div([
        html.H1("Compare Two Datasets and Calculate Z-Statistic Value"), # Header
        html.Div([ 
            html.H3("Enter Data for Population 1"), # Sub-Header
            create_data_table_two_col('data-table1', zdf1, 'Population 1'), # Table 1
            html.Button("Add Row to Population 1", id="add-row-btn1", n_clicks=0), # Updating
        ]),
        html.Div([
            html.H3("Enter Data for Population 2"), # Sub-Header
            create_data_table_two_col('data-table2', zdf2, 'Population 2'), # Table 2
            html.Button("Add Row to Population 2", id="add-row-btn2", n_clicks=0), # Updating
        ]),
        html.Button("Update Box Plot and Z-Statistic", id="update-plot-btn", n_clicks=0),
        dcc.Graph(id='box-plot'), # Creating the box-plot
        html.H3("Z-Statistic Result"), # Sub-header
        html.Div(id='z-test-result') # Styling
    ])

    # Updating the Z-test Population 1 Data Table
    @dash_ztest_app.callback(
        Output('data-table1', 'data'), # Making Table
        Input('add-row-btn1', 'n_clicks'), # Adding rows to the table
        State('data-table1', 'data') # Updating the table
    )
    def add_row_population1(n_clicks, data1):
        """
        Adds a new row with default values to the Population 1 data table 
        when the "Add Row to Population 1" button is clicked.

        Args:
            - n_clicks (int): The number of times the add row button has been clicked.
            - data1 (list of dict): Current data for Population 1, where each
                dictionary represents a row with 'X Values' and 'Z Values' keys.

        Returns:
            list of dict: Updated data1 list with a new row appended if `n_clicks` > 0.
                        The new row has an incremented 'X Values' and a 'Z Values' 
                        initialized to 0.
        """
        if n_clicks > 0:
            data1.append({'X Values': len(data1) + 1, 'Z Values': 0})
        return data1

    # Updating the Z-test Population 1 Data Table
    @dash_ztest_app.callback(
        Output('data-table2', 'data'), # Making the Table
        Input('add-row-btn2', 'n_clicks'), # Adding rows to the table
        State('data-table2', 'data') # Updating the table
    )
    def add_row_population2(n_clicks, data2):
        """
        Adds a new row with default values to the Population 2 data table 
        when the "Add Row to Population 2" button is clicked.

        Args:
            - n_clicks (int): The number of times the add row button has been clicked.
            - data2 (list of dict): Current data for Population 2, where each
                dictionary represents a row with 'X Values' and 'Z Values' keys.

        Returns:
            list of dict: Updated data2 list with a new row appended if `n_clicks` > 0.
                        The new row has an incremented 'X Values' and a 'Z Values' 
                        initialized to 0.
        """
        if n_clicks > 0:
            data2.append({'X Values': len(data2) + 1, 'Z Values': 0})
        return data2

    # Z-test Plot
    @dash_ztest_app.callback(
        Output('box-plot', 'figure'), # Making the Box-plot
        Output('z-test-result', 'children'), # Text Result
        Input('update-plot-btn', 'n_clicks'), # Adding Rows
        State('data-table1', 'data'), # Updating Dataset 1
        State('data-table2', 'data') # Updating Dataset 2
    )

    def update_ztest_plot(n_clicks, data1, data2):
        """
        Updates the box plot and calculates the z-statistic for 
        two populations when the "Update Box Plot and Z-Statistic" 
        button is clicked.

        Args:
            - n_clicks (int): Click count for the update button, 
                triggering the update.
            - data1 (list of dict): Data for Population 1, from the 
                interactive table, with 'X Values' and 'Population 1' keys.
            - data2 (list of dict): Data for Population 2, from the interactive 
                table, with 'X Values' and 'Population 2' keys.

        Returns:
            - figure (plotly.graph_objs.Figure): Box plot comparing 
                the distributions of Population 1 and Population 2.
            - z_test_result_text (str): Calculated z-statistic and 
                p-value or a message if data variance is insufficient.
        """
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

    # Making the Distribution Page figures
    dash_distribution_app = Dash(__name__, server=flask_app,
                                 routes_pathname_prefix="/dash_distribution/")
    dist_data = plots.generate_distribution_data()

    # Formatting Distribution Data Table
    dash_distribution_app.layout = html.Div([
        html.H1("Data for Distribution Plot"),
        create_data_table_one_col('Distribution Data', dist_data, 'Values'),
        dcc.Graph(id='hist-chart', style={'width': '60%', 'margin': '10 auto'})
    ])

    # Distribution Plot
    @dash_distribution_app.callback(
        Output('hist-chart', 'figure'),
        Input('Distribution Data', 'data')
    )

    def update_distribution_plot(dist_data1):
        """This function generates a histogram based on a
        user-provided input values. As the user changes
        the inputted values, the plot will change. 

        Args:
            data1: Web app user inputted numbers

        Returns:
            figure: the new updated plot is outputted.
        """
        return plots.generate_distribution_plot(dist_data1)

    # ANOVA Test Figures
    dash_anova_app = Dash(__name__, server=flask_app, routes_pathname_prefix='/dash_anova/')

    # Data Generation for ANOVA Test
    def initialize_anova_data(rows=30):
        """
        Generates random data for three sample populations 
        with values between 80 and 100.

        Args:
            - rows (int): The number of data points (rows) to generate.
                Defaults to 30.

        Returns:
            - pd.DataFrame: DataFrame with 'X Values', 'Population 1', 
                'Population 2', and 'Population 3'.
        """
        data = {
            'X Values': list(range(1, rows + 1)),
            'Population 1': np.random.randint(80, 101, rows),
            'Population 2': np.random.randint(80, 101, rows),
            'Population 3': np.random.randint(80, 101, rows),
        }
        return pd.DataFrame(data)

    anova_df = initialize_anova_data(30)

    # Data Table Function for Three Populations
    def create_data_table_three_col(table_id, anova_df):
        """This function creates a table of data with three columns of data for the 
        user to see and interact with on the web app page.
        
        Args:
            table_id (int): table identifying number 
            data (list): dataframe of information for the table

        Returns:
            dictionary: table information for the dash app to format
        """
        return dash_table.DataTable(
            id=table_id,
            columns=[
                {'name': 'X Values', 'id': 'X Values', 'editable': True},
                {'name': 'Population 1', 'id': 'Population 1', 'editable': True},
                {'name': 'Population 2', 'id': 'Population 2', 'editable': True},
                {'name': 'Population 3', 'id': 'Population 3', 'editable': True},
            ],
            data=anova_df.to_dict('records'),
            editable=True,
            row_deletable=False,
            style_table={'overflowX': 'auto'}
        )

    # ANOVA Data Table
    dash_anova_app.layout = html.Div([
        html.H1("Compare Three Datasets and Calculate ANOVA F-Statistic Value"),

        # Single Data Table for all populations
        html.Div([
            html.H3("Enter Data for All Populations"),
            create_data_table_three_col('data-table1', anova_df),  # Just use one DataFrame now
            html.Button("Add Row", id="add-row-btn1", n_clicks=0),
        ]),

        html.Button("Update Box Plot and ANOVA Test", id="update-plot-btn", n_clicks=0),
        dcc.Graph(id='box-plot'),
        html.H3("ANOVA Test Result"),
        html.Div(id='anova-test-result')
    ])

    # Updating the ANOVA Data Table
    @dash_anova_app.callback(
        Output('data-table1', 'data'),
        Input('add-row-btn1', 'n_clicks'),
        State('data-table1', 'data')
    )
    def add_row_to_all_populations(n_clicks, data):
        """
        Adds a new row with default values to the consolidated data table
        when the "Add Row" button is clicked.

        Args:
            - n_clicks (int): The number of times the add row button has been clicked.
            - data (list of dict): Current data for all populations, where each dictionary is a
                row with 'X Values', 'Population 1', 'Population 2', and 'Population 3' keys.

        Returns:
            list of dict: Updated data list with a new row appended if `n_clicks` > 0.
                The new row has an incremented 'X Values' and initialized population values.
        """
        if n_clicks > 0:
            next_x_value = len(data) + 1
            data.append({'X Values': next_x_value,
                         'Population 1': 0,
                         'Population 2': 0,
                         'Population 3': 0})
        return data

    # ANOVA Plot
    @dash_anova_app.callback(
        Output('box-plot', 'figure'),
        Output('anova-test-result', 'children'),
        Input('update-plot-btn', 'n_clicks'),
        State('data-table1', 'data')
    )
    def update_anova_plot(n_clicks, data):
        """
        Updates the box plot and calculates the ANOVA test statistic for 
        three populations when the "Update Box Plot and ANOVA Test" 
        button is clicked.

        Args:
            - n_clicks (int): Click count for the update button, 
                triggering the update.
            - data (list of dict): Data for all populations, from the interactive table,
                 with 'X Values', 'Population 1', 'Population 2', and 'Population 3' keys.

        Returns:
            - figure (plotly.graph_objs.Figure): Box plot comparing 
                the distributions of Population 1, Population 2, and Population 3.
            - anova_result_text (str): Calculated ANOVA F-statistic and 
                p-value or a message if data variance is insufficient.
        """
        print("update button clicked:", n_clicks)  # Debug statement

        if n_clicks > 0:
            # Convert data to numeric, ignoring non-numeric values
            data_frame = pd.DataFrame(data).apply(pd.to_numeric, errors='coerce').fillna(0)

            # Check data values before proceeding (debugging)
            print("Data Frame:\n", data_frame)

            # Separate the populations
            pop1 = data_frame['Population 1']
            pop2 = data_frame['Population 2']
            pop3 = data_frame['Population 3']

            figure, anova_result_text = plots.generate_anova_plot(pop1, pop2, pop3)
            return figure, anova_result_text

        return go.Figure(), "No update requested."

    dash_regressions_app = Dash(__name__, server=flask_app, routes_pathname_prefix='/dash_regressions/')

    linear_df = plots.initialize_linear_data()

    # Layout for the Linear Regression page
    dash_regressions_app.layout = html.Div([
        html.H1("Interactive Linear Regression"),
        html.Div([
            html.H3("Edit Data Table"),
            dash_table.DataTable(
                id='linear-data-table',
                columns=[
                    {'name': 'X Values', 'id': 'X Values', 'editable': True},
                    {'name': 'Y Values', 'id': 'Y Values', 'editable': True},
                ],
                data=linear_df.to_dict('records'),
                editable=True,
                row_deletable=False,
                style_table={'overflowX': 'auto'}
            ),
            html.Button("Add Row", id="add-row-btn", n_clicks=0),
        ]),
        html.Button("Update Plot", id="update-regression-plot-btn", n_clicks=0),
        dcc.Graph(id='linear-regression-plot'),
        html.H3("Linear Regression Equation"),
        html.Div(id='linear-regression-equation', style={'fontSize': '18px', 'marginTop': '20px'}),
        html.H3("R² Value"),
        html.Div(id='linear-regression-r2', style={'fontSize': '18px', 'marginTop': '10px'}),
    ])

    # Callback to update regressions data table
    @dash_regressions_app.callback(
        Output('linear-data-table', 'data'),
        Input('add-row-btn', 'n_clicks'),
        State('linear-data-table', 'data')
    )

    def add_row(n_clicks, current_data):
        """
        Adds a new row to the linear regression data table when the "Add Row" button is clicked.

        Args:
            n_clicks (int): Number of times the button has been clicked.
            current_data (list of dict): Current data in the data table.

        Returns:
            list of dict: Updated data with a new row appended.
        """
        if n_clicks > 0:
            next_x_value = len(current_data) + 1  # Increment X Value
            current_data.append({'X Values': next_x_value, 'Y Values': 0})  # Add new row
        return current_data

    # Callback to update the plot and display the regression equation
    @dash_regressions_app.callback(
        [Output('linear-regression-plot', 'figure'),
         Output('linear-regression-equation', 'children'),
         Output('linear-regression-r2', 'children')],
        [Input('update-regression-plot-btn', 'n_clicks')],
        [State('linear-data-table', 'data')]
    )

    def update_linear_regression_plot(n_clicks, data):
        """
        Updates the linear regression plot and displays the equation and R² value 
        when the "Update Plot" button is clicked.

        Args:
            n_clicks (int): Number of times the update button has been clicked.
            data (list of dict): Data for the regression table.

        Returns:
            - plotly.graph_objs.Figure: The updated regression plot.
            - str: The linear regression equation or a placeholder message.
            - str: The R² value or a placeholder message.
        """
        if n_clicks and n_clicks > 0:
            # Generate the plot, equation, and R² value
            figure, equation, r2_value = plots.generate_linear_regression_plot(data)
            return (
                figure,
                f"Linear Regression Equation: {equation}",
                f"R² Value: {r2_value:.4f}"
            )
        
        # Default state before updates
        return go.Figure(), "No updates requested.", "No updates requested."

    return {
        'dash_test': dash_test_app,
        'dash_ttest': dash_ttest_app,
        'dash_ztest': dash_ztest_app,
        'dash_distribution': dash_distribution_app,
        'dash_anova': dash_anova_app,
        'dash_regressions': dash_regressions_app
    }

def create_data_table_two_col(table_id, data, value_col):
    """This function creates the table of data with two columns of data for the 
    user to see and interact with on the web app page.

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
        style_table={'overflowX': 'auto'}
    )

def create_data_table_one_col(table_id, data, value_col):
    """This function creates the tables of data for the 
    user to see and interact with on the web app page.

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
            {'name': value_col, 'id': value_col, 'editable': True}
        ],
        data=data.to_dict('records'),
        editable=True,
        row_deletable=False,
        style_table={
            'overflowX': 'auto',  # Horizontal scrolling if the table is wider than the container
            'maxWidth': '600px',   # Limit the max width of the table (set as appropriate)
            'width': 'auto',       # Ensure the table width adapts to the content
        },
        style_cell={
            'textAlign': 'center',  # Center align the text
            'padding': '5px',
            'minWidth': '50px',    # Set a minimum width for the column
            'width': 'auto',        # Allow the column to resize dynamically based on content
        },
    )

