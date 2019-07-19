import binascii
import datetime

from bitarray import bitarray

from app.models import ValveConfiguration


def convert_to_emi(val):
    hex_val = '{0:04X}'.format(val)
    inv = hex_val[2:] + hex_val[:2]
    return inv


def convert_to_html_timestamp(timestamp):
    date = datetime.date(timestamp.year, timestamp.month, timestamp.day)
    time = datetime.time(timestamp.hour, timestamp.minute, timestamp.second)
    s = date.isoformat()
    s += "T"
    s += time.isoformat()
    return s

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
            print(stamp)
            ##  Write Year
            f.write(binascii.unhexlify(convert_to_emi(stamp.year)))
            ##  Write Month
            print(convert_to_emi(stamp.month))
            f.write(binascii.unhexlify(convert_to_emi(stamp.month)))
            ##  Write Day
            print(convert_to_emi(stamp.day))
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
            for i in range(6):
                # Convert each 16 bits to int
                byte = data[j - 16:j]
                ba = bitarray('0' * 16, endian='little')
                for it in range(len(byte)):
                    ba[it] = int(byte[it])
                value = 0
                for bit in ba:
                    value = (value << 1) | bit
                # Convert int to hex
                f.write(binascii.unhexlify(convert_to_emi(value)))
                j = j + 16
            ### Fill row
            for i in range(6):
                f.write(binascii.unhexlify(convert_to_emi(0)))
            ##
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
            j = 8
            for i in range(len(data) / 8):
                byte = data[j - 8:j]
                ba = bitarray('0' * 8, endian='little')
                for it in range(len(byte)):
                    ba[it] = int(byte[it])
                value = 0
                for bit in ba:
                    value = (value << 1) | bit
                f.write(str(value))
                f.write('\n')
                j = j + 8
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
        if int(data[i - 1]) == 1:
            prev_checked.append(i)
    return prev_checked


'''
Returns the date of a timestamp
'''


def getDate(timestamp):
    return datetime.date(timestamp.year, timestamp.month, timestamp.day)


def getTime(timestamp):
    return datetime.time(timestamp.hour, timestamp.minute, timestamp.second)


def diff(t1, t2):
    hdiff = t1.hour - t2.hour
    mdiff = t1.minute - t2.minute
    sdiff = t1.second - t2.second
    return hdiff + mdiff + sdiff
