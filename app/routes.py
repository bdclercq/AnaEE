import subprocess
import json

from flask import render_template, request, redirect
from sqlalchemy import desc

from app import app, db
from app.AnaEEUtils import *

##############################
fs = ['fati1', 'fati2', 'fati3', 'fati4', 'fati5', 'fati6', 'fati7', 'fati8',
      'fati9', 'fati10', 'fati11', 'fati12']
vs = []
vn = []
bs2 = ""
for i in range(1, 97):
    name = "valve"
    name = name + str(i)
    vs.append(name)
    vn.append(i)
    bs2 += "0"
    ##############################


@app.route('/')
@app.route('/home')
def home():
    vcs = ValveConfiguration.query.order_by(ValveConfiguration.timestamp).all()
    times = []
    statuses = []
    for vc in vcs:
        s = convert_to_html_timestamp(vc.timestamp)
        times.append(s)
        statuses.append(vc.status)
    return render_template('home.html', size=len(times), times=times, stats=statuses, fatis=fs, valves=vs,
                           valvenumbers=vn)


@app.route('/configure/<timestmp>', methods=['POST', 'GET'])
@app.route('/configure/', methods=['POST', 'GET'])
def configure(timestmp=None):
    if timestmp is None:
        tmstmp = request.form['datetime']
    else:
        tmstmp = timestmp
    timestamp = convert_timestamp(tmstmp)
    exists = db.session.query(ValveConfiguration.timestamp).filter_by(timestamp=timestamp).scalar() is not None
    if exists:
        data = ValveConfiguration.query.filter_by(timestamp=timestamp).first()
        numbers = convert_data(data)
        return render_template('configure.html', timestamp=tmstmp, data=data, nrs=numbers, fatis=fs, valves=vs,
                               valvenumbers=vn)
    if not exists:
        return render_template('configure.html', timestamp=tmstmp, fatis=fs, valves=vs, valvenumbers=vn)


@app.route('/commit_config/<timestamp>', methods=['POST', 'GET'])
def commit_config(timestamp):
    if request.method == 'POST':
        result = request.form
        generate_end = False
        if len(result.getlist("generateEnd")) > 0:
            generate_end = True
        timestamp = convert_timestamp(timestamp)
        # print(result)
        checked_valves = []
        for v in vs:
            # print(result.getlist(v))
            if len(result.getlist(v)) > 0:
                for vi in range(len(result.getlist(v))):
                    checked_valves.append(int(result.getlist(v)[vi]))
        # print(checked_valves)
        ##############################
        bs = ''
        for i in range(1, 97):
            if i in checked_valves:
                bs = bs + '1'
            else:
                bs = bs + '0'
        # print(bs)
        # print(bs2)
        ##############################
        exists = db.session.query(ValveConfiguration.timestamp).filter_by(timestamp=timestamp).scalar() is not None
        if not exists:
            vc = ValveConfiguration(timestamp=timestamp, status=bs)
            # print(timestamp)
            db.session.add(vc)
            db.session.commit()
            if generate_end:
                timestamp = timestamp + datetime.timedelta(seconds=int(json.load(open("app/misc.json", 'r'))["settings"]["on_time"]))
                # print(timestamp)
                vc2 = ValveConfiguration(timestamp=timestamp, status=bs2, configtype=0)
                db.session.add(vc2)
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
    p = subprocess.Popen(['python', './app/fileSelect.py'], stdin=subprocess.PIPE, stdout=subprocess.PIPE,
                         universal_newlines=True)
    out, err = p.communicate()
    export_data(out.strip())
    return redirect("/")


@app.route('/writetoemi', methods=['POST', 'GET'])
def writetoemi():
    p = subprocess.Popen(['python', './app/fileSelect.py'], stdin=subprocess.PIPE, stdout=subprocess.PIPE,
                         universal_newlines=True)
    out, err = p.communicate()
    # print(out.strip())
    export_data_emi(out.strip())
    return redirect("/")


@app.route('/remove/<timestamp>', methods=['POST', 'GET'])
def remove(timestamp):
    vc = ValveConfiguration.query.filter_by(timestamp=convert_timestamp(timestamp)).first()
    db.session.delete(vc)
    db.session.commit()
    return redirect("/")


@app.route('/duplication/<timestamp>', methods=['POST', 'GET'])
def duplication(timestamp):
    return render_template("/duplicate.html", old=timestamp)


@app.route('/duplicate/<old>', methods=['POST', 'GET'])
def duplicate(old):
    new_date = request.form['newdate']
    old = convert_timestamp(old)
    conf = ValveConfiguration.query.filter_by(timestamp=old).first()
    year = int(new_date[0:4])
    month = int(new_date[5:7])
    day = int(new_date[8:10])
    date = datetime.date(year, month, day)
    time = datetime.time(old.hour, old.minute, old.second)
    new_stamp = datetime.datetime.combine(date, time)
    vc = ValveConfiguration(timestamp=new_stamp, status=conf.status)
    db.session.add(vc)
    db.session.commit()
    return redirect("/")


@app.route('/overview')
def overview():
    data = {}
    confs = ValveConfiguration.query.order_by(ValveConfiguration.timestamp).all()
    # print(len(confs))
    for conf in confs:
        year, month, day = getDate(conf.timestamp)
        if year not in data:
            data[year] = {}
        if month not in data[year]:
            data[year][month] = {}
        if day not in data[year][month]:
            data[year][month][day] = {}
            for v in range(96):
                data[year][month][day][v] = {}
                data[year][month][day][v]['latest'] = 0
                data[year][month][day][v]['value'] = 0
        time = conf.timestamp.time
        status = conf.status
        for i in range(96):
            if status[i] == '1':
                # print(1)
                if data[year][month][day][i]['latest'] == 0:
                    data[year][month][day][i]['latest'] = time
            elif status[i] == '0':
                # print(0)
                if data[year][month][day][i]['latest'] != 0:
                    data[year][month][day][i]['value'] = diff(time, data[year][month][day][i]['latest'])
                    data[year][month][day][i]['latest'] = 0
    # print(data)
    return redirect("/")


@app.route('/misc', methods=['POST', 'GET'])
def misc():
    data = json.load(open("app/misc.json", 'r'))
    print(data)
    return render_template("misc.html", data=data)


@app.route('/change_misc', methods=['POST'])
def change_misc():
    if request.method == 'POST':
        on_time = request.form['on_time']
        shift_days = request.form['shift_days']
        move_days = request.form['move_days']
        data = json.load(open("app/misc.json", 'r'))
        on_diff = int(on_time) - int(data["settings"]["on_time"])
        print(on_time, data["settings"]["on_time"], on_diff)
        vcs = ValveConfiguration.query.order_by(ValveConfiguration.timestamp).all()
        for vc in vcs:
            if vc.configtype == 0:
                print(vc.timestamp, vc.timestamp + datetime.timedelta(seconds=int(on_diff)))
                vc.timestamp = vc.timestamp + datetime.timedelta(seconds=int(on_diff))
                db.session.commit()
        data["settings"]["on_time"] = on_time
        data["settings"]["shift_days"] = shift_days
        data["settings"]["move_days"] = move_days
        json.dump(data, open("app/misc.json", 'w'))
        return redirect("/misc")
    else:
        return redirect("/misc")


@app.route('/shift_entries', methods=["POST"])
def shift_entries():
    result = request.form.to_dict()
    print(result)
    print(len(result.items()))

    # Move entries
    if len(list(result.items())) == 3:
        key, val = list(result.items())[0]
        key2, val2 = list(result.items())[1]
        action = list(result.items())[2]
        print(action)
        print(type(action))
        vcs = ValveConfiguration.query \
            .filter(ValveConfiguration.timestamp >= convert_timestamp(key)) \
            .filter(ValveConfiguration.timestamp <= convert_timestamp(key2)) \
            .order_by(desc(ValveConfiguration.timestamp)).all()
        if action[1] == "Move":
            for vc in vcs:
                timestamp = vc.timestamp + datetime.timedelta(
                    days=int(json.load(open("app/misc.json", 'r'))["settings"]["move_days"]))
                vc2 = ValveConfiguration(timestamp=timestamp, status=vc.status, configtype=vc.configtype)
                print(vc, vc2)
                db.session.add(vc2)
                db.session.commit()
            return redirect('/')
        else:
            err = "Oops, something went wrong.\n"
            if action[1] == "Shift":
                err += "You selected 2 items and clicked on 'Shift'. \n" \
                      "Please select one item less or click 'Move' next time."
            else:
                err += "Something went wrong (@app.route('shift_entries'), Move entries part). \n" \
                      "Are you sure you selected 2 items and clicked 'Move'?"
            return render_template('400.html', err=err)
    # Shit entries
    elif len(list(result.items())) == 2:
        key, val = list(result.items())[0]
        action = list(result.items())[1]
        print(action)
        print(type(action))
        vcs = ValveConfiguration.query \
            .filter(ValveConfiguration.timestamp >= convert_timestamp(key)) \
            .order_by(desc(ValveConfiguration.timestamp)).all()
        if action[1] == "Shift":
            for vc in vcs:
                vc.timestamp += datetime.timedelta(
                    days=int(json.load(open("app/misc.json", 'r'))["settings"]["shift_days"]))
                print(vc)
                db.session.commit()
            return redirect('/')
        else:
            err = "Oops, something went wrong.\n"
            if action[1] == "Move":
                err += "You selected 1 item and clicked on 'Move'. \n" \
                       "Please select one item more or click 'Shift' next time."
            else:
                err += "Something went wrong (@app.route('shift_entries'), Shift entries part). \n" \
                      "Are you sure you selected 1 item and clicked 'Shift'?"
            return render_template('400.html', err=err)
    # Return error
    else:
        err = "Too many items checked at once, please try again by checking less items"
        return render_template('400.html', err=err)
