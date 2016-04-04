from sensor import getMeasurments
from measurmentsDB import addMeasurment
import logging as log
log.basicConfig(format='%(asctime)s %(message)s', filename='sensor.log', level=log.DEBUG)

if __name__ == '__main__':
    try:
        measurments = getMeasurments()
    except:
        log.debug('first try failed...')

    if measurments is None:
        try:
            measurments = getMeasurments()
        except:
            log.debug('second try failed...')

    if measurments is not None:
        log.info('measurments: {0}'.format(measurments))
        addMeasurment(*measurments)
