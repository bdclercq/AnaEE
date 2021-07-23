import binascii
import datetime
import csv

from app.models import ValveConfiguration
from app import app, db

fatis = 12
valves = 12


##############################
### CHECK TIMESTAMPS
##############################

def check_stamp_lower(stamp, f, v):
    vcs = ValveConfiguration.query.filter_by(timestamp=stamp).all()
    for vc in vcs:
        if vc.status[(f*valves)+v] == '0':
            return True
    return False


def check_stamp_higher(stamp, f, v):
    vcs = ValveConfiguration.query.filter_by(timestamp=stamp).all()
    for vc in vcs:
        if vc.status[(f*valves)+v] == '1':
            return True
    return False


##############################
### CONVERT TIMESTAMP
##############################

def convert_to_html_timestamp(timestamp):
    date = datetime.date(timestamp.year, timestamp.month, timestamp.day)
    time = datetime.time(timestamp.hour, timestamp.minute, timestamp.second)
    s = date.isoformat()
    s += "T"
    s += time.isoformat()
    return s


##############################
### CHECK OVERVIEW FOR ERRORS
##############################

def check_overview(data, limits):
    problems = {'lower': [], 'higher': [], 'lower_valves': [], 'higher_valves': []}
    for k in data.keys(): # Date
        for f in data[k].keys(): # Fati
            for v in data[k][f].keys(): # Valve
                if data[k][f][v]['run_time'] < limits['min_target']:
                    # get entries for this day
                    for stamp in data[k][f][v]['stamps']:
                        if check_stamp_lower(stamp, f, v):# and stamp not in problems['lower']:
                            problems['lower'].append(stamp)
                            problems['lower_valves'].append((f*valves)+v)
                elif data[k][f][v]['run_time'] > limits['max_target']:
                    # get entries for this day
                    for stamp in data[k][f][v]['stamps']:
                        if check_stamp_higher(stamp, f, v):# and stamp not in problems['higher']:
                            problems['higher'].append(stamp)
                            problems['higher_valves'].append((f * valves) + v)
    return problems


##############################
### CONVERT VALUES
##############################

def convert_to_emi(val):
    hex_val = '{0:04X}'.format(val)
    inv = hex_val[2:] + hex_val[:2]
    return inv


def convert_to_dec(inv):
    hex_val = inv[2:] + inv[:2]
    dec_val = int(hex_val, 16)
    return dec_val


def flipbits(x):
    #reverse bits in a byte#
    x1 = x << 4 | x >4
    x2 = (x1 & 51) << 2 | (x1 & 204) >2
    return (x2 & 85) << 1 | (x2 & 170) >1


##############################
### EXPORT DATABASE
##############################
'''
Export data to emi format
'''


def export_data_emi(filename):
    if filename != '':
        # Open file in binary mode to avoid write bug
        f = open(filename, "wb")
        ##############################
        # Get all configurations and sort by increasing timestamp
        configs = ValveConfiguration.query.order_by(ValveConfiguration.timestamp).all()
        config_id = 0
        # Write each configuration to file
        for conf in configs:
            config_id = config_id + 1
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
            # j: bits that can be addressed
            j = 12
            # 12*12 == 144 ( == valves*fatis)
            for i in range(12):
                # Convert each 16 bits to int
                byte = flipbits(data[j - 12:j])
                byte += '0000'
                ba = []
                for it in range(len(byte)):
                    ba.append(int(byte[it]))
                value = 0
                print(ba)
                for bit in ba:
                    value = (value << 1) | bit
                # Convert int to hex
                f.write(binascii.unhexlify(convert_to_emi(value)))
                j = j + 12
            ### Add marking for begin or end
            #f.write(binascii.unhexlify(convert_to_emi(conf.configtype)))
            # ### Fill row (row doesn't need to be filled anymore, the six 'free' slots have been filled)
            # for i in range(6):
            #     f.write(binascii.unhexlify(convert_to_emi(0)))
            ##
            f.write(binascii.unhexlify(convert_to_emi(0)))
            #f.write(binascii.unhexlify(convert_to_emi(0)))
            #f.write(binascii.unhexlify(convert_to_emi(0)))
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
<configtype>
0
0
0
<sequence number>
...
'''


def export_data(filename):
    if filename != '':
        f = open(filename, "w+")
        ##############################
        # Get all configurations and sort by increasing timestamp
        configs = ValveConfiguration.query.order_by(ValveConfiguration.timestamp).all()
        config_id = 0
        # Write each configuration to file
        for conf in configs:
            config_id = config_id + 1
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
            j = valves
            for i in range(int(len(data) / valves)):
                byte = data[j - valves:j]
                ba = []
                for it in range(len(byte)):
                    ba.append(int(byte[it]))
                value = 0
                for bit in ba:
                    value = (value << 1) | bit
                f.write(str(value))
                f.write('\n')
                # f.write(str(conf.configtype))
                # f.write('\n')
                j = j + valves
            f.write(str(conf.configtype))
            f.write('\n')
            ### Fill row
            for i in range(3):
                f.write(str(0))
                f.write('\n')
        ##############################
        f.close()


##############################
### IMPORT DATABASE
##############################

'''
Imports data from a CSV file
'''


def import_data_csv(filename, overwrite):
    if filename != '':
        first = True
        with open(filename, mode='r') as csv_file:
            csv_reader = csv.DictReader(csv_file)
            line_count = 1
            skip = 1
            record = {"id": 0, "year": 0, "month": 0, "day": 0, "hour": 0, "minute": 0, "second": 0, "f1": 0,
                      "f2": 0, "f3": 0, "f4": 0, "f5": 0, "f6": 0, "f7": 0, "f8": 0, "f9": 0, "f10": 0,
                      "f11": 0, "f12": 0, "status": 0}
            keys = {"0": "id", "1": "year", "2": "month", "3": "day", "4": "hour", "5": "minute", "6": "second",
                    "11": "f1", "12": "f2", "13": "f3", "14": "f4", "15": "f5", "16": "f6", "17": "f7", "18": "f8",
                    "19": "f9", "20": "f10", "21": "f11", "22": "f12", "23": "status"}
            for row in csv_reader:
                if first:
                    if line_count <= 6:
                        record[keys[str(line_count)]] = row['1']
                        line_count += 1
                    elif 6 < line_count < 11:
                        line_count += 1
                    elif 11 <= line_count <= 23:
                        if skip:
                            record[keys[str(line_count)]] = row['1']
                            skip = 0
                            line_count += 1
                        else:
                            skip = 1
                    elif 23 < line_count < 27:
                        line_count += 1
                    elif line_count == 27:
                        print(record)
                        date = datetime.date(int(record["year"]), int(record["month"]), int(record["day"]))
                        time = datetime.time(int(record["hour"]), int(record["minute"]), int(record["second"]))
                        timestamp = datetime.datetime.combine(date, time)
                        exists = db.session.query(ValveConfiguration.timestamp).filter_by(
                            timestamp=timestamp).scalar() is not None
                        # Skip existing entries
                        if not exists:
                            bs = ''
                            for i in range(11, 23):
                                bs += "{0:16b}".format(int(record[keys[str(i)]]))
                            # bs += '0000000'
                            vc = ValveConfiguration(timestamp=timestamp, status=bs, configtype=int(record[keys[str(23)]]))
                            db.session.add(vc)
                            db.session.commit()
                        line_count = 0
                        skip = 1
                        first = False
                else:
                    if 0 <= line_count <= 6:
                        record[keys[str(line_count)]] = row['1']
                        line_count += 1
                    elif 6 < line_count < 11:
                        line_count += 1
                    elif 11 <= line_count <= 23:
                        if skip:
                            record[keys[str(line_count)]] = row['1']
                            line_count += 1
                            skip = 0
                        else:
                            skip = 1
                    elif 23 < line_count < 25:
                        line_count += 1
                    elif line_count == 25:
                        print(record)
                        date = datetime.date(int(record["year"]), int(record["month"]), int(record["day"]))
                        time = datetime.time(int(record["hour"]), int(record["minute"]), int(record["second"]))
                        timestamp = datetime.datetime.combine(date, time)
                        conftype = record["status"]
                        exists = db.session.query(ValveConfiguration.timestamp).filter_by(
                            timestamp=timestamp).scalar() is not None
                        # Skip existing entries
                        if not exists:
                            bs = ''
                            for i in range(11, 23):
                                bs += "{0:16b}".format(int(record[keys[str(i)]]))
                            # bs += '0000000'
                            vc = ValveConfiguration(timestamp=timestamp, status=bs, configtype=conftype)
                            db.session.add(vc)
                        if overwrite == "1":
                            vc = ValveConfiguration.query.filter(ValveConfiguration.timestamp == timestamp).first()
                            vc.status = bs
                            vc.configtype = conftype
                        db.session.commit()
                        line_count = 0
                        skip = 1


def import_data_emi(filename, overwrite):
    if filename != '':
        count = 0
        #print(overwrite)
        with open(filename, mode='rb') as emi_file:
            record = ["id", "year", "month", "day", "hour", "minute", "second", "f1", "f2", "f3", "f4", "f5", "f6",
                      "f7", "f8", "f9", "status"]
            value = emi_file.read(2)
            while value != '':
                try:
                    # print(value)
                    # print(convert_to_dec(binascii.hexlify(value)))
                    # Only the first 16 values have meaning
                    if count <= 16:
                        valve = convert_to_dec(binascii.hexlify(value))
                        record[count] = valve
                        value = emi_file.read(2)
                        count += 1
                    elif 17 <= count < 19:
                        # Contains only zero values
                        value = emi_file.read(2)
                        count += 1
                    elif count == 19:
                        print(record)
                        # Read last zero
                        value = emi_file.read(2)
                        # Write record to db
                        date = datetime.date(int(record[1]), int(record[2]), int(record[3]))
                        time = datetime.time(int(record[4]), int(record[5]), int(record[6]))
                        timestamp = datetime.datetime.combine(date, time)
                        exists = db.session.query(ValveConfiguration.timestamp).filter_by(
                            timestamp=timestamp).scalar() is not None
                        bs = ''
                        # 144 (12 fatis * 12 valves) divided by 16 (bits) equals 9
                        for i in range(7, 16):
                            bs += "{0:016b}".format(int(record[i]))
                        # bs += '0000000'
                        conftype = int(record[16])
                        print(bs)
                        # Skip existing entries
                        if not exists:
                            #print("Adding record with type {0}".format(conftype))
                            vc = ValveConfiguration(timestamp=timestamp, status=bs, configtype=conftype)
                            db.session.add(vc)
                        if overwrite == "1":
                            vc = ValveConfiguration.query.filter(ValveConfiguration.timestamp == timestamp).first()
                            vc.status = bs
                            vc.configtype = conftype
                        db.session.commit()
                        value = emi_file.read(2)
                        print(value)
                        print(convert_to_dec(binascii.hexlify(value)))
                        print("------------------")
                        count = 1
                except ValueError as e:
                    value = ''
                    print("Import EMI error: ValueError encountered: ", e)


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
    for i in range(1, (fatis*valves)+1):
        if int(data[i - 1]) == 1:
            prev_checked.append(i)
    return prev_checked


'''
Returns the date of a timestamp
'''


def getDate(timestamp):
    return datetime.date(timestamp.year, timestamp.month, timestamp.day)


'''
Returns the time of a timestamp
'''


def getTime(timestamp):
    return datetime.time(timestamp.hour, timestamp.minute, timestamp.second)
