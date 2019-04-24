import datetime

from flask import Flask, render_template
from flask_restful import Resource, Api, reqparse, fields, marshal_with
import http.client, urllib.request, urllib.parse, urllib.error, base64
import requests

from models.Fati import Fati

parser = reqparse.RequestParser()

app = Flask(__name__)
api = Api(app)

fatis = []

@app.route('/')
@app.route('/home/')
def home():
    if len(fatis)==0:
        for i in range(12):
            name = "fati_"
            name += str(i)
            fatis.append(Fati(name, i))
    return render_template('home.html', data=fatis)


@app.route('/fati/<number>')
def fati(number):
    return render_template('fati.html', fati=fatis[int(number)])

@app.route('/fati/<fati>/<valve>')
def valve(fati, valve):
    return render_template('valve.html', valve=fatis[int(fati)].get_valve(int(valve)))


if __name__ == '__main__':
    app.run(debug=True)
