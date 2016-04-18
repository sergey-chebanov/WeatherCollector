from flask import Flask, request, g, render_template
import sqlite3
from measurmentsDB import readMeasurments
from collections import namedtuple

app = Flask(__name__)


@app.before_request
def before_request():
    g.db = sqlite3.connect('weather.db', detect_types=sqlite3.PARSE_DECLTYPES|sqlite3.PARSE_COLNAMES)


@app.teardown_request
def teardown_request(exception):
    db = getattr(g, 'db', None)
    if db is not None:
        db.close()

Measurement = namedtuple('Measurement', ['date', 'T', 'H', 'P'])

@app.route('/pressure/')
def pressure():
    limit = int(request.args.get('limit', 72))
    data = readMeasurments(limit, desc=False)
    return render_template('pressure.html', data=(Measurement(*row) for row in data))

@app.route('/test/')
def index():
    limit = int(request.args.get('limit', 144))
    data = readMeasurments(limit, desc=False)
    measurements = [Measurement(*row) for row in data]
    *_, recent = measurements
    return render_template('index.html', data=measurements, recent=recent)

@app.route('/')
def measurments():
    limit = int(request.args.get('limit', 20))
    data = readMeasurments(limit)
    result = ''
    for row in data:
        result += "{0:02}:{1:02} T={2} H={3} P={4}<br/>".format(row[0].hour, row[0].minute, row[1], row[2], row[3])

    return result


if __name__ == "__main__":
    app.run(debug=True, host='0.0.0.0')
