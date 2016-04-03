import sqlite3
import time
from datetime import date, datetime


conn = sqlite3.connect('weather.db', detect_types=sqlite3.PARSE_DECLTYPES|sqlite3.PARSE_COLNAMES)

c = conn.cursor()

def addMeasurment (temp, hum, pres):
    c.execute("insert into measurments (time, temp, hum, pres) values (?,?,?,?)", (datetime.now(), temp, hum, pres))
    conn.commit()


def readLastMeasurment():
    #get the record
    c.execute ("select time, temp, hum, pres from measurments order by rowid desc")
    row = c.fetchone()
    return row


def readMeasurments():
    c.execute ("select time, temp, hum, pres from measurments order by rowid desc")
    for row in c:
        print ("{0} {1} {2}".format(row[0].year, row[0].hour, row[0].second))
        for v in row:
            print("{0} {1}".format(v, type(v)))
