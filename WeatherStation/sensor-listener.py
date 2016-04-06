import sys
import time
import traceback
from sensor import getMeasurments
from measurmentsDB import addMeasurment
import logging as log
log.basicConfig(format='%(asctime)s %(message)s', filename='sensor.log', level=log.DEBUG)

if __name__ == '__main__':
    for x in range(3):
        try:
            log.debug('try {} ...'.format(x))
            measurments = getMeasurments()
            if measurments is not None:
                log.debug('try {} succeded: {}'.format(x, measurments))
                addMeasurment(*measurments)
                break
            else:
                time.sleep(5*2**x)
        except:
            traceback.print_exc()
            log.error("{}".format(sys.exc_info()))
        log.debug('try {} failed...'.format(x))
