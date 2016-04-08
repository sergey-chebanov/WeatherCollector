import serial
import sys
import time
import re
import logging as log
from contextlib import closing

log.basicConfig(format='%(asctime)s %(message)s', filename='sensor.log', level=log.DEBUG)

SENSOR_MAC='98:D3:31:20:6D:74'

import bluetooth
def commandBT(cmd):
    with closing(bluetooth.BluetoothSocket(bluetooth.RFCOMM)) as btSocket:
        btSocket.connect((SENSOR_MAC, 1))
        btSocket.send(cmd)
        btSocket.settimeout(2)
        time.sleep(2)
        s = btSocket.recv(1024)
        log.debug('{}'.format(s))
        return s.decode('UTF8')

def commandSerial(cmd):
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

command = commandBT

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
        result = (temp, hum, pres)
        return tuple(round(float(i), 2) for i in result)

if __name__ == '__main__':
    print(command('t'))
