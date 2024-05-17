#!/usr/bin/python3
"""scrpt that starts a FLAsk web application"""
from flask import Flask
from markupsafe import escape
app = Flask(__name__)


@app.route('/', strict_slashes=False)
def hello_hbnb():
    """Routing to root"""
    return "Hello HBNB!"


@app.route('/hbnb', strict_slashes=False)
def hbnb():
    """Routing to /hbnb"""
    return "HBNB"


@app.route('/c/<text>', strict_slashes=False)
def display_text(text):
    """Display text """
    text = text.replace("_", " ")
    return f"C {escape(text)}"


@app.route('/python/', defaults={'text': 'is_cool'}, strict_slashes=False)
@app.route('/python/<text>', strict_slashes=False)
def python_text(text="is cool"):
    text = text.replace("_", " ")
    return f"Python {escape(text)}"


@app.route('/number/<n>', strict_slashes=False)
def number_display(n):
    return "{} is a number".format(n)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
