import sys
import time
import traceback
from sensor import getMeasurements
from MeasurementsDB import addMeasurement
import logging as log
log.basicConfig(format='%(asctime)s %(message)s', filename='sensor.log', level=log.DEBUG)

if __name__ == '__main__':
    for x in range(3):
        try:
            log.debug('try {} ...'.format(x))
            measurments = getMeasurements()
            if measurments is not None:
                log.debug('try {} succeded: {}'.format(x, measurments))
                addMeasurement(*measurments)
                break
            else:
                time.sleep(5*2**x)
        except:
            traceback.print_exc()
            log.error("{}".format(sys.exc_info()))
        log.debug('try {} failed...'.format(x))
