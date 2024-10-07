from flask import Flask, render_template, request
from waitress import serve

app = Flask(__name__)


@app.route('/')

@app.route('/home')
def home():
    return render_template('home.html')


@app.route('/example_page')
def example_simulation():
    concept = request.args.get('concept')
    return render_template(
        "example_page.html",
        title=concept
    )


if __name__ == "__main__":
    serve(app, host="0.0.0.0", port=8000)
