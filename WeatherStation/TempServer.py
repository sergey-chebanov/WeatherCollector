from flask import Flask, request, g, render_template
import sqlite3
from MeasurementsDB import readMeasurements, readWaterMeasurements
from collections import namedtuple
from datetime import datetime

app = Flask(__name__)


@app.before_request
def before_request():
    g.db = sqlite3.connect('weather.db', detect_types=sqlite3.PARSE_DECLTYPES|sqlite3.PARSE_COLNAMES)
    g.water_db = sqlite3.connect('../../waterSensor/waterDB.sqlite', detect_types=sqlite3.PARSE_DECLTYPES|sqlite3.PARSE_COLNAMES)



@app.teardown_request
def teardown_request(exception):

    def close_db(db_name):
        db = getattr(g, db_name, None)
        if db is not None:
            db.close()

    close_db('db')
    close_db('water_db')

Measurement = namedtuple('Measurement', ['date', 'T', 'H', 'P'])


@app.route('/pressure/')
def pressure():
    limit = int(request.args.get('limit', 72))
    data = readMeasurements(limit, desc=False)
    return render_template('pressure.html', data=(Measurement(*row) for row in data))


GraphPoint = namedtuple("GraphPoint", ['dt','cold', 'hot'])

@app.route('/water/')
def water():
    days = int(request.args.get('hours', 24))
    relative = bool(request.args.get('relative', 0))

    cold_water = readWaterMeasurements(0, days, relative)
    hot_water = readWaterMeasurements(1, days, relative)

    if 0:
        counter = [min(i.counter for i in water_ms if i.type ==0), min(i.counter for i in water_ms if i.type ==1) ]
        points = []
        for m in water_ms:
            if m.counter > counter[m.type]:
                counter [m.type] = m.counter
            points += [GraphPoint(dt=m.dt, cold=counter[0], hot=counter[1])]

    #print (points)

    return render_template('water.html',
        cold_water=cold_water,
        hot_water=hot_water,
        recent_hot=cold_water[-1].counter,
        recent_cold=hot_water[-1].counter,
        date = datetime.now()
        )


@app.route('/weather/')
def index():
    limit = int(request.args.get('limit', 144))
    data = readMeasurements(limit, desc=False)
    measurements = [Measurement(*row) for row in data]
    *_, recent = measurements
    return render_template('index.html', data=measurements, recent=recent)

@app.route('/test/')
def Measurements():
    limit = int(request.args.get('limit', 20))
    data = readMeasurements(limit)
    result = ''
    for row in data:
        result += "{0:02}:{1:02} T={2} H={3} P={4}<br/>".format(row[0].hour, row[0].minute, row[1], row[2], row[3])

    return result


if __name__ == "__main__":
    app.run(debug=True, host='0.0.0.0')
