from flask import Flask, request, g, render_template
import sqlite3
from MeasurementsDB import readMeasurements, readWaterMeasurements
from collections import namedtuple

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

WaterMeasurement = namedtuple('WaterMeasurement', ['date', 'hot', 'cold'])

@app.route('/pressure/')
def pressure():
    limit = int(request.args.get('limit', 72))
    data = readMeasurements(limit, desc=False)
    return render_template('pressure.html', data=(Measurement(*row) for row in data))

@app.route('/water/')
def water():
    limit = int(request.args.get('limit', 72))
    water_ms = [WaterMeasurement(*row) for row in readWaterMeasurements(limit, desc=False)]

    if 0:
        result = ''
        for row in data:
            wm = WaterMeasurement(*row)
            result += "D={} H={} C={}<br/>".format(wm.date, wm.hot, wm.cold)

        return result

    return render_template('water.html', data=water_ms)


@app.route('/test/')
def index():
    limit = int(request.args.get('limit', 144))
    data = readMeasurements(limit, desc=False)
    measurements = [Measurement(*row) for row in data]
    *_, recent = measurements
    return render_template('index.html', data=measurements, recent=recent)

@app.route('/')
def Measurements():
    limit = int(request.args.get('limit', 20))
    data = readMeasurements(limit)
    result = ''
    for row in data:
        result += "{0:02}:{1:02} T={2} H={3} P={4}<br/>".format(row[0].hour, row[0].minute, row[1], row[2], row[3])

    return result


if __name__ == "__main__":
    app.run(debug=True, host='0.0.0.0')
