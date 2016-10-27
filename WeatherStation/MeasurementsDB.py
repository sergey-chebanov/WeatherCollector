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

def addLabeledValues (labeled_values):
    with closing(sqlite3.connect('weather.db', detect_types=sqlite3.PARSE_DECLTYPES|sqlite3.PARSE_COLNAMES)) as conn:
        c = conn.cursor()
        for label, value in labeled_values:
            c.execute(
                    "insert into labeled_measurements (time, label, value)"
                    "values (?,?,?)", (datetime.now(), label, value))
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


WaterMeasurement = namedtuple('WaterMeasurement', ['dt', 'counter', 'type'])

def _dt_isoformat (dt):
    return dt.isoformat() + "Z"

_direction = {'left': ("<=", "desc"), 'right': (">=", "asc")}

Base = namedtuple('Base', ['real_counter', 'counter'])
def _to_rc(c, base):
    return base.real_counter + (c - base.counter)


def _read_base_counter (type, dt):

    with closing(g.water_db.cursor()) as c:
        c.execute("select datetime, real_counter from base_counter where type=? and datetime < ? order by datetime desc limit 1;", (type, dt))
        [(base_dt, base_real_counter), *_] = c.fetchall()

        c.execute("select counter from water where type=? and datetime {} ? order by datetime {} limit 1;".format(*_direction ['left']), (type, base_dt))
        [(base_counter,), *_] = c.fetchall()

        return Base(base_real_counter, base_counter)

def _get_current_counter (type, dt, base):

    with closing(g.water_db.cursor()) as c:
        #get end point counter
        c.execute("select counter from water where type=? and datetime {} ? order by datetime {} limit 1;".format(*_direction ['left']), (type, dt))
        [(counter,), *_] = c.fetchall()

        print (counter, base)

        return _to_rc(counter, base)


def readWaterMeasurements(type, hours, relative):

    with closing (g.water_db.cursor()) as c:

        now = datetime.utcnow()
        dt_from = now - timedelta(hours = hours)

        print ("from {} to {}".format(dt_from, now))

        rows = []


        base = Base(*_read_base_counter(type, dt_from))

        if relative:
            base = Base(0, base.counter)

        print (base)

        for dt in (dt_from, now):
            real_counter = _get_current_counter(type, _dt_isoformat(dt), base)
            point = WaterMeasurement(_dt_isoformat(dt), real_counter, type)
            print (point)
            rows += [point,]

        query = 'select datetime as t, counter, type from (select datetime, counter, type from water where type = ? and datetime > ? and datetime < ? order by datetime desc) order by t'


        rows += [WaterMeasurement(dt = row[0], type = row[2], counter = _to_rc(row[1], base)) for row in c.execute(query, (type, _dt_isoformat(dt_from), _dt_isoformat(now)))]


        rows = sorted(rows, key=lambda r: r.dt)
        print ("--------- Rows ---------")
        for row in rows:
            print(row)
        return rows
