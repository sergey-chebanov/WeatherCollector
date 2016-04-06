import serial
import sys
import time
import re
import logging as log
log.basicConfig(format='%(asctime)s %(message)s', filename='sensor.log', level=log.DEBUG)

def command(cmd):
    with serial.Serial('/dev/rfcomm0', baudrate=9600, timeout=2) as ser:
        ser.flush()
        ser.write(cmd)
        ser.flush()
        result = []
        time.sleep(1)
        #log.debug('inWaiting {}'.format(ser.inWaiting()))
        while ser.inWaiting() > 0:
            s = ser.readline()
            log.debug('{}'.format(s))
            result.append (s.strip())
            time.sleep(0.1)
        return result

def getMeasurments():
    rawMeasurments = ''.join(command ('m'))
    log.debug('raw input: {}'.format(rawMeasurments))
    try:
        temp, hum, temp2, _, pres = rawMeasurments.split(':')
        temp = (float(temp2) + float(temp)) / 2
    except ValueError:
        return None
    except:
        log.error("{}".format(sys.exc_info()))
        raise
    else:
        log.debug('{} {} {}'.format(temp, hum, pres))
        return (temp, float(hum), float(pres))

if __name__ == '__main__':
    print(command('t'))
