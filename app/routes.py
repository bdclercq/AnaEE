from flask import render_template, request, redirect
from app import app, db
from app.models import ValveConfiguration
import datetime


@app.route('/')
def home():
    return render_template('admin.html')


@app.route('/commit_config', methods=['POST', 'GET'])
def commit_config():
    if request.method == 'POST':
        result = request.form
        timestamp = result['datetime']
        year = int(timestamp[0:4])
        month = int(timestamp[5:7])
        day = int(timestamp[8:10])
        date = datetime.date(year, month, day)
        hour = int(timestamp[11:13])
        minute = int(timestamp[14:16])
        second = int(timestamp[17:])
        time = datetime.time(hour, minute, second)
        timestamp = datetime.datetime.combine(date, time)
        config = bytearray(16)
        print(timestamp)
        ##############################
        fatis = []
        if 'fati1' in result:
            fatis.append(1)

        if 'fati2' in result:
            fatis.append(2)

        if 'fati3' in result:
            fatis.append(3)

        if 'fati4' in result:
            fatis.append(4)

        if 'fati5' in result:
            fatis.append(5)

        if 'fati6' in result:
            fatis.append(6)

        if 'fati7' in result:
            fatis.append(7)

        if 'fati8' in result:
            fatis.append(8)

        if 'fati9' in result:
            fatis.append(9)

        if 'fati10' in result:
            fatis.append(10)

        if 'fati11' in result:
            fatis.append(11)

        if 'fati12' in result:
            fatis.append(12)

        ##############################
        valvebyte = 0
        if 'valve1' in result:
            valvebyte = valvebyte | 1

        if 'valve2' in result:
            valvebyte = valvebyte | 2

        if 'valve3' in result:
            valvebyte = valvebyte | 4

        if 'valve4' in result:
            valvebyte = valvebyte | 8

        if 'valve5' in result:
            valvebyte = valvebyte | 16

        if 'valve6' in result:
            valvebyte = valvebyte | 32

        if 'valve7' in result:
            valvebyte = valvebyte | 64

        if 'valve8' in result:
            valvebyte = valvebyte | 128

        ##############################


        print(valvebyte)
        for f in fatis:
            config[f] = valvebyte
        print(config)
        exists = db.session.query(ValveConfiguration.timestamp).filter_by(timestamp=timestamp).scalar() is not None
        if not exists:
            vc = ValveConfiguration(timestamp=timestamp, status=config)
            db.session.add(vc)
            db.session.commit()
        print(ValveConfiguration.query.all())
    return redirect("/")
