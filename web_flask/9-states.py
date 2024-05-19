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


@app.route('/states', strict_slashes=False)
def states():
    """
    fetches data from sql database and renders in html template
    """
    states = storage.all(State)
    return render_template('9-states.html', state=states)


@app.route('/states/<id>', strict_slashes=False)
def states_id(id):
    """Displays an HTML page with info about id if it exists"""
    for state in storage.all(State).values():
        if state.id == id:
            return render_template("9-states.html", state=state)
    return render_template("9-states.html")


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
