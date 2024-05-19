#!/usr/bin/python3
"""script that fetch data from sql database and render to html"""
from flask import Flask, render_template
from models import storage
from models.state import State

app = Flask(__name__)


@app.teardown_appcontext
def teardown(self):
    """
    removes the current sqlalchemy session
    """
    storage.close()


@app.route('/cities_by_states', strict_slashes=False)
def cities_by_state():
    """
    fetches data from sql database and renders in html template
    """
    states = storage.all(State)
    return render_template('8-cities_by_states.html', states=states)


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
