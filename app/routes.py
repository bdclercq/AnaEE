from flask import render_template, request, redirect
from app import app, db
from app.models import ValveConfiguration
import datetime, threading
import Tkinter, tkFileDialog

fs = ['fati1', 'fati2', 'fati3', 'fati4', 'fati5', 'fati6', 'fati7', 'fati8',
              'fati9', 'fati10', 'fati11', 'fati12']
vs = []
vn = []
for i in range(1, 97):
    name = "valve"
    name = name+str(i)
    vs.append(name)
    vn.append(i)

def export_data():
    root = Tkinter.Tk()
    # root.withdraw()
    filename = tkFileDialog.askopenfilename()
    if filename != '' :
        f = open(filename, "w+")
        # print(filename)
        ##############################
        configs = ValveConfiguration.query.order_by(ValveConfiguration.timestamp).all()
        config_id = 0
        for conf in configs:
            config_id = config_id+1
            f.write(str(config_id))
            f.write('\n')
            ### Write timestamp
            stamp = conf.timestamp
            ##  Write Year
            f.write(str(stamp.year))
            f.write('\n')
            ##  Write Month
            f.write(str(stamp.month))
            f.write('\n')
            ##  Write Day
            f.write(str(stamp.day))
            f.write('\n')
            ##  Write Hour
            f.write(str(stamp.hour))
            f.write('\n')
            ##  Write Minutes
            f.write(str(stamp.minute))
            f.write('\n')
            ##  Write Seconds
            f.write(str(stamp.second))
            f.write('\n')
            ### Fill row
            for i in range(4):
                f.write(str(0))
                f.write('\n')
            ### Add data
            data = conf.status
            j = 8
            for i in range(len(data)/8):
                for d in data[j-8:j]:
                    f.write(d)
                f.write('\n')
                j = j+8
            ### Fill row
            for i in range(4):
                f.write(str(0))
                f.write('\n')
        ##############################
        f.close()

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
        # print(data[i-1])
        if int(data[i-1]) == 1:
            prev_checked.append(i)
    # print(prev_checked)
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
        # print(data)
        numbers = convert_data(data)
        return render_template('configure.html', timestamp=tmstmp, data=data, nrs=numbers, fatis=fs, valves=vs, valvenumbers=vn)
    if not exists:
        return render_template('configure.html', timestamp=tmstmp, fatis=fs, valves=vs, valvenumbers=vn)

@app.route('/commit_config/<timestamp>', methods=['POST', 'GET'])
def commit_config(timestamp):
    if request.method == 'POST':
        result = request.form
        timestamp = convert_timestamp(timestamp)
        # print(timestamp)
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
        # print(bs)
        exists = db.session.query(ValveConfiguration.timestamp).filter_by(timestamp=timestamp).scalar() is not None
        if not exists:
            vc = ValveConfiguration(timestamp=timestamp, status=bs)
            db.session.add(vc)
            db.session.commit()
        else:
            config = ValveConfiguration.query.filter_by(timestamp=timestamp).first()
            config.status = bs
            db.session.commit()
        # print(ValveConfiguration.query.all())
    return redirect("/")


@app.route('/export')
def export():
    return render_template('export.html')

@app.route('/writetofile', methods=['POST', 'GET'])
def writetofile():
    x = threading.Thread(target=export_data)
    x.start()
    # x.join()
    return redirect("/")
