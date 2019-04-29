from flask import render_template
from app import app


@app.route('/')
@app.route('/home/')
def home():
    return render_template('home.html', data=[])


@app.route('/fati/<number>')
def fati(number):
    return render_template('fati.html', fati=None)


@app.route('/fati/<fati>/<valve>')
def valve(fati, valve):
    return render_template('valve.html', valve=None)
