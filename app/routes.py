from flask import render_template, request, redirect
from app import app, db
from app.models import ValveConfiguration
import threading
from app.AnaEEUtils import *

        ##############################
fs = ['fati1', 'fati2', 'fati3', 'fati4', 'fati5', 'fati6', 'fati7', 'fati8',
              'fati9', 'fati10', 'fati11', 'fati12']
vs = []
vn = []
for i in range(1, 97):
    name = "valve"
    name = name+str(i)
    vs.append(name)
    vn.append(i)
        ##############################

@app.route('/')
@app.route('/home')
def home():
    vcs = ValveConfiguration.query.order_by(ValveConfiguration.timestamp).all()
    times=[]
    statuses=[]
    for vc in vcs:
        times.append(str(vc.timestamp))
        statuses.append(vc.status)
    return render_template('home.html', size=len(times), times=times, stats=statuses, fatis=fs, valves=vs, valvenumbers=vn)

@app.route('/configure', methods=['POST', 'GET'])
def configure():
    tmstmp = request.form['datetime']
    timestamp = convert_timestamp(tmstmp)
    exists = db.session.query(ValveConfiguration.timestamp).filter_by(timestamp=timestamp).scalar() is not None
    if exists:
        data = ValveConfiguration.query.filter_by(timestamp=timestamp).first()
        numbers = convert_data(data)
        return render_template('configure.html', timestamp=tmstmp, data=data, nrs=numbers, fatis=fs, valves=vs, valvenumbers=vn)
    if not exists:
        return render_template('configure.html', timestamp=tmstmp, fatis=fs, valves=vs, valvenumbers=vn)

@app.route('/commit_config/<timestamp>', methods=['POST', 'GET'])
def commit_config(timestamp):
    if request.method == 'POST':
        result = request.form
        timestamp = convert_timestamp(timestamp)
        print(result)
        checked_valves = []
        for v in vs:
            print(result.getlist(v))
            if len(result.getlist(v)) > 0:
                for vi in range(len(result.getlist(v))):
                    checked_valves.append(int(result.getlist(v)[vi]))
        print(checked_valves)
        ##############################
        bs = ''
        for i in range(1, 97):
            if i in checked_valves:
                bs = bs+'1'
            else:
                bs = bs+'0'
        print(bs)
        ##############################
        exists = db.session.query(ValveConfiguration.timestamp).filter_by(timestamp=timestamp).scalar() is not None
        if not exists:
            vc = ValveConfiguration(timestamp=timestamp, status=bs)
            db.session.add(vc)
            db.session.commit()
        else:
            config = ValveConfiguration.query.filter_by(timestamp=timestamp).first()
            config.status = bs
            db.session.commit()
    return redirect("/")

@app.route('/export')
def export():
    return render_template('export.html')

@app.route('/writetocsv', methods=['POST', 'GET'])
def writetocsv():
    x = threading.Thread(target=export_data)
    x.start()
    return redirect("/")\

@app.route('/writetoemi', methods=['POST', 'GET'])
def writetoemi():
    x = threading.Thread(target=export_data_emi)
    x.start()
    x.join()
    return redirect("/")
