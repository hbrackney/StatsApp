from flask import Flask, render_template, redirect, url_for, request
from waitress import serve

app = Flask(__name__)

options = {
    't-test': 'ttest',
    'z-test': 'ztest'
}

@app.route('/') # Home Page
def home():
    return render_template('home.html', options=options)

@app.route('/submit', methods=['POST']) # Submitting Dropdown menu Option
def submit():
    selected_option = request.form.get('options')
    if selected_option in options:
        return redirect(url_for(options[selected_option]))
    return redirect(url_for('home'))

@app.route('/ttest')
def ttest():
    return render_template('ttest.html')

@app.route('/ztest')
def ztest():
    return render_template('ztest.html')

if __name__ == "__main__":
    serve(app, host="0.0.0.0", port=8000)
