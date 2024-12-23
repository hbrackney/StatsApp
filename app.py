"""This is the app intialization page."""

from flask import Flask, render_template, redirect, url_for, request #, jsonify
from waitress import serve
from dash_apps import create_dash_apps

# Intialize Flask App
app = Flask(__name__)

# List of Pages -> make sure if page name is changed, the html file matches
pages = ["home", "about", "ttest", "z_test_page", "distributions_page",
         "anova", "regressions", "reference_page"]

# Home Page Dropdown Menu Options
options = {
    "t-test": pages[2],
    "z-test": pages[3],
    "Data Distributions": pages[4],
    "ANOVA test": pages[5],
    "Regressions": pages[6]
}

create_dash_apps(app)

# App Routes
@app.route("/")  # Home Page
def home(options_list=options):
    """This function renders the home page.

    Returns: Creates the home page
    """
    return render_template(f"{pages[0]}.html", options=options_list)

@app.route("/about")  # About Page
def about():
    """This function renders the about page.

    Returns: Creates the about page
    """
    return render_template(f"{pages[1]}.html")


# Routing for Clicking on a button
@app.route("/submit", methods=["POST"])
def submit(options_list=options):
    """This function submits the drop
    down box entry and takes you to the home page.

    Returns: redirects to  home page
    """
    selected_option = request.form.get("options")
    if selected_option in options_list:
        return redirect(url_for(options_list[selected_option]))
    return redirect(url_for(pages[0]))

@app.route(f"/{pages[2]}", methods=['GET', 'POST']) # T-test Page
def ttest():
    """This function renders the t test page or handles POST requests."""
    return render_template(f'{pages[2]}.html')

@app.route(f"/{pages[3]}") # Z-Test Page
def z_test_page():
    """This function renders the z test page.

    Returns: Creates the z test page
    """
    return render_template(f'{pages[3]}.html')

@app.route(f"/{pages[4]}") # Distributions Page
def distributions_page():
    """This function renders the Data Distributions page.

    Returns: Creates the Data Distributions page
    """
    return render_template(f'{pages[4]}.html')

@app.route(f"/{pages[5]}") # ANOVA Page
def anova():
    """This function renders the ANOVA page.

    Returns: Creates the ANOVA page
    """
    return render_template(f'{pages[5]}.html')

@app.route(f"/{pages[6]}") # Regressions Page
def regressions():
    """This function renders the regressions page.

    Returns: Creates the regressions page
    """
    return render_template(f'{pages[6]}.html')

@app.route(f"/{pages[7]}") # Example page
def example_page():
    """This function renders the interactive test
    page. This page serves as an example for any users
    who want to contribute to the project and add a
    new statisical concept.

    Returns: Creates the interactive page
    """
    return render_template(f"{pages[7]}.html")

# Change this port # below if the terminal says that the Address is already in use.
# If you change port #, update the README Usage instrcutions to reflect the new number
if __name__ == "__main__":
    serve(app, host="0.0.0.0", port=1000) # port number
