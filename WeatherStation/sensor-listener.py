import sys
import time
import traceback
from sensor import getMeasurements
from MeasurementsDB import addMeasurement, addLabeledValues
import logging as log
log.basicConfig(format='%(asctime)s %(message)s', filename='sensor.log', level=log.DEBUG)

if __name__ == '__main__':
    for x in range(3):
        try:
            log.debug('try {} ...'.format(x))
            mss = getMeasurements()
            if mss is not None:
                temp, hum, pres, co2 = mss
                data = (["T", temp], ["H", hum], ["co2", co2], ["P", pres])
                log.debug('try {} succeded: {}'.format(x, mss))
                addMeasurement(temp, hum, pres)
                addLabeledValues(data)
                break
            else:
                time.sleep(5*2**x)
        except:
            traceback.print_exc()
            log.error("{}".format(sys.exc_info()))
        log.debug('try {} failed...'.format(x))
