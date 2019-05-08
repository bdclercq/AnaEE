from flask import render_template, request, redirect
from app import app, db
from app.models import ValveConfiguration
import datetime, threading
import Tkinter, tkFileDialog
import binascii
from bitarray import bitarray

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

def convert_to_emi(val):
    hex_val = '{0:04X}'.format(val)
    inv = hex_val[2:] + hex_val[:2]
    return inv

'''
Export data to emi format
'''
def export_data_emi():
    filename = tkFileDialog.askopenfilename()
    if filename != '' :
        f = open(filename, "w+")
        ##############################
        # Get all configurations and sort by increasing timestamp
        configs = ValveConfiguration.query.order_by(ValveConfiguration.timestamp).all()
        config_id = 0
        # Write each configuration to file
        for conf in configs:
            config_id = config_id+1
            f.write(binascii.unhexlify(convert_to_emi(config_id)))
            ### Write timestamp
            stamp = conf.timestamp
            ##  Write Year
            f.write(binascii.unhexlify(convert_to_emi(stamp.year)))
            ##  Write Month
            f.write(binascii.unhexlify(convert_to_emi(stamp.month)))
            ##  Write Day
            f.write(binascii.unhexlify(convert_to_emi(stamp.day)))
            ##  Write Hour
            f.write(binascii.unhexlify(convert_to_emi(stamp.hour)))
            ##  Write Minutes
            f.write(binascii.unhexlify(convert_to_emi(stamp.minute)))
            ##  Write Seconds
            f.write(binascii.unhexlify(convert_to_emi(stamp.second)))
            ### Add data
            data = conf.status
            j = 16
            for i in range(len(data)/16):
                # Convert each 16 bits to int
                byte = data[j-16:j]
                ba = bitarray('0'*16, endian='little')
                for it in range(len(byte)):
                    ba[it]=int(byte[it])
                value = 0
                for bit in ba:
                    value = (value << 1) | bit
                # Convert int to hex
                f.write(binascii.unhexlify(convert_to_emi(value)))
                j = j+16
            ### Fill row
            f.write(binascii.unhexlify(convert_to_emi(3)))
            for i in range(4):
                f.write(binascii.unhexlify(convert_to_emi(0)))
        ##############################
        f.close()

'''
Function that will write all data from the database to a chosen file.
The output file will be a CSV file with following format:
<sequence number>
<year>
<month>
<day>
<hour>
<minute>
<second>
0
0
0
0
<decimal value of byte 1>
<decimal value of byte 2>
<decimal value of byte 3>
...
<decimal value of byte 12>
0
0
0
0
<sequence number>
...
'''
def export_data():
    filename = tkFileDialog.askopenfilename()
    if filename != '' :
        f = open(filename, "w+")
        ##############################
        # Get all configurations and sort by increasing timestamp
        configs = ValveConfiguration.query.order_by(ValveConfiguration.timestamp).all()
        config_id = 0
        # Write each configuration to file
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
                byte = data[j-8:j]
                ba = bitarray('0'*8, endian='little')
                for it in range(len(byte)):
                    ba[it]=int(byte[it])
                value = 0
                for bit in ba:
                    value = (value << 1) | bit
                f.write(str(value))
                f.write('\n')
                j = j+8
            ### Fill row
            for i in range(4):
                f.write(str(0))
                f.write('\n')
        ##############################
        f.close()

'''
Converts the HTML timestamp to a Python timestamp
'''
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

'''
Converts the data so it can be stored in the database
'''
def convert_data(data):
    prev_checked = []
    data = data.status
    for i in range(1, 97):
        if int(data[i-1]) == 1:
            prev_checked.append(i)
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
    return redirect("/")
