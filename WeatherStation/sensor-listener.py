from sensor import getMeasurments
from measurmentsDB import addMeasurment


if __name__ == '__main__':
    measurments = getMeasurments()
    print(measurments)
    if measurments is not None:
        addMeasurment(*measurments)
