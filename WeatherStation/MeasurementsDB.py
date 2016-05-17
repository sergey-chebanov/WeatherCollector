import time
import sqlite3
from datetime import date, datetime
from flask import g
from contextlib import closing


def addMeasurement (temp, hum, pres):
    with closing(sqlite3.connect('weather.db', detect_types=sqlite3.PARSE_DECLTYPES|sqlite3.PARSE_COLNAMES)) as conn:
        c = conn.cursor()
        c.execute("insert into measurements (time, temp, hum, pres) values (?,?,?,?)", (datetime.now(), temp, hum, pres))
        conn.commit()


def readLastMeasurement():
    #get the record
    c = g.db.cursor()
    c.execute ("select time, temp, hum, pres from measurements order by rowid desc")
    row = c.fetchone()
    return row


def readMeasurements(limit = 20, desc=True):
    c = g.db.cursor()
    c.execute ("select * from (select time, temp, hum, pres from measurements order by time desc limit ?) order by time {sort}".format(sort='desc' if desc else 'asc'), (limit,))
    return [row for row in c]


def readWaterMeasurements(limit = 20, desc=True):
    c = g.water_db.cursor()
    c.execute ('select datetime as t, hot, cold from (select datetime, hot, cold from water order by datetime desc limit ?) order by t;'.format(sort='desc' if desc else 'asc'), (limit,))
    return [row for row in c]
