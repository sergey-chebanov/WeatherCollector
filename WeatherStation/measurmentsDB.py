import time
import sqlite3
from datetime import date, datetime
from flask import g
from contextlib import closing


def addMeasurment (temp, hum, pres):
    with closing(sqlite3.connect('weather.db', detect_types=sqlite3.PARSE_DECLTYPES|sqlite3.PARSE_COLNAMES)) as conn:
        c = conn.cursor()
        c.execute("insert into measurments (time, temp, hum, pres) values (?,?,?,?)", (datetime.now(), temp, hum, pres))
        conn.commit()


def readLastMeasurment():
    #get the record
    c = g.db.cursor()
    c.execute ("select time, temp, hum, pres from measurments order by rowid desc")
    row = c.fetchone()
    return row


def readMeasurments(limit = 20):
    c = g.db.cursor()
    c.execute ("select time, temp, hum, pres from measurments order by rowid desc limit ?", (limit,))
    return [row for row in c]
