"""This is the app intialization page."""

from flask import Flask, render_template, redirect, url_for, request, jsonify
from waitress import serve
from dash_apps import create_dash_apps

# Intialize Flask App
app = Flask(__name__)

# Home Page Dropdown Menu Options
options = {
    "t-test": "ttest",
    "z-test": "z_test_page"
}

create_dash_apps(app)

# App Routes
@app.route("/")  # Home Page
def home():
    """This function renders the home page.

    Returns: Creates the home page
    """
    return render_template("home.html", options=options)

@app.route("/about")  # Home Page
def about():
    """This function renders the about page.

    Returns: Creates the about page
    """
    return render_template("about.html", options=options)

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


@app.route("/ttest", methods=['GET', 'POST'])
def ttest():
    """This function renders the t test page or handles POST requests."""
    return render_template('ttest.html')


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

if __name__ == "__main__":
    serve(app, host="0.0.0.0", port=14000)