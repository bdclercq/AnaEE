from flask import render_template, request, redirect
from app import app, db
from app.models import ValveConfiguration
import datetime
from Tkinter import Tk
from tkinter.filedialog import askopenfilename

fs = ['fati1', 'fati2', 'fati3', 'fati4', 'fati5', 'fati6', 'fati7', 'fati8',
              'fati9', 'fati10', 'fati11', 'fati12']
vs = []
vn = []
for i in range(1, 97):
    name = "valve"
    name = name+str(i)
    vs.append(name)
    vn.append(i)


def convert_timestamp(timestamp):
    year = int(timestamp[0:4])
    month = int(timestamp[5:7])
    day = int(timestamp[8:10])
    date = datetime.date(year, month, day)
    hour = int(timestamp[11:13])
    minute = int(timestamp[14:16])
    if timestamp[17:] == '':
        second = 00
    else:
        second = int(timestamp[17:])
    time = datetime.time(hour, minute, second)
    timestamp = datetime.datetime.combine(date, time)
    return timestamp


def convert_data(data):
    prev_checked = []
    data = data.status
    for i in range(1, 97):
        print(data[i-1])
        if int(data[i-1]) == 1:
            prev_checked.append(i)
    print(prev_checked)
    return prev_checked


@app.route('/')
@app.route('/home')
def home():
    return render_template('home.html')

@app.route('/configure', methods=['POST', 'GET'])
def configure():
    tmstmp = request.form['datetime']
    timestamp = convert_timestamp(tmstmp)
    exists = db.session.query(ValveConfiguration.timestamp).filter_by(timestamp=timestamp).scalar() is not None
    if exists:
        data = ValveConfiguration.query.filter_by(timestamp=timestamp).first()
        print(data)
        numbers = convert_data(data)
        return render_template('configure.html', timestamp=tmstmp, data=data, nrs=numbers, fatis=fs, valves=vs, valvenumbers=vn)
    if not exists:
        return render_template('configure.html', timestamp=tmstmp, fatis=fs, valves=vs, valvenumbers=vn)

@app.route('/commit_config/<timestamp>', methods=['POST', 'GET'])
def commit_config(timestamp):
    if request.method == 'POST':
        result = request.form
        timestamp = convert_timestamp(timestamp)
        print(timestamp)
        checked_valves = []
        for v in vs:
            if len(result.getlist(v)) > 0:
                checked_valves.append(int(result.getlist(v)[0]))
        ##############################
        bs = ''
        for i in range(1, 97):
            if i in checked_valves:
                bs = bs+'1'
            else:
                bs = bs+'0'
        ##############################
        print(bs)
        exists = db.session.query(ValveConfiguration.timestamp).filter_by(timestamp=timestamp).scalar() is not None
        if not exists:
            vc = ValveConfiguration(timestamp=timestamp, status=bs)
            db.session.add(vc)
            db.session.commit()
        else:
            config = ValveConfiguration.query.filter_by(timestamp=timestamp).first()
            config.status = bs
            db.session.commit()
        print(ValveConfiguration.query.all())
    return redirect("/")


@app.route('/export')
def export():
    return render_template('export.html')

@app.route('/writetofile', methods=['POST', 'GET'])
def writetofile():
    filename = request.form['configfile']
    f = open(filename, "w+")
    ##############################
    configs = ValveConfiguration.query.order_by(ValveConfiguration.timestamp).all()
    for conf in configs:
        ### Write timestamp
        stamp = conf.timestamp
        ##  Write Year
        f.write(stamp.year)
        f.write(',')
        ##  Write Month
        f.write(stamp.month)
        f.write(',')
        ##  Write Day
        f.write(stamp.day)
        f.write(',')
        ##  Write Hour
        f.write(stamp.hour)
        f.write(',')
        ##  Write Minutes
        f.write(stamp.minute)
        f.write(',')
        ##  Write Seconds
        f.write(stamp.second)
        f.write(',')
        ### Fill row
        for i in range(4):
            f.write(0)
            f.write(',')
        ### Add data
        data = conf.status
        for d in data:
            f.write(d)
            f.write(',')
        ### Fill row
        for i in range(4):
            f.write(0)
            f.write(',')
    ##############################
    f.close()
