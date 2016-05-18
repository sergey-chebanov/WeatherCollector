import time
import sqlite3
from datetime import date, datetime, timedelta
from flask import g
from contextlib import closing
from collections import namedtuple



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


WaterMeasurement = namedtuple('WaterMeasurement', ['date', 'hot', 'cold'])

def readWaterMeasurements(days = 1):

    c = g.water_db.cursor()

    now = datetime.utcnow()
    n_days_before = now - timedelta(days)

    c.execute('select count(*) from water where datetime > "{}"'.format(n_days_before.isoformat() + 'Z'));
    [(count,)] = c.fetchall()

    #get all elements for the days and an extra
    c.execute ('select datetime as t, hot, cold from (select datetime, hot, cold from water order by datetime desc limit ?) order by t;', (count+1,))

    rows = [WaterMeasurement(*row) for row in c]
    _, hot, cold = rows.pop(0)
    rows.insert(0, WaterMeasurement(n_days_before.isoformat() + 'Z', hot, cold))
    _, hot, cold = rows [-1]
    rows.append (WaterMeasurement (now.isoformat() + 'Z', hot, cold))

    return rows
