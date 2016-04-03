import serial
import time
import re


def command(cmd):
	ser = serial.Serial('/dev/rfcomm0', baudrate=115200)
	ser.timeout = 2
	ser.write(cmd)
	ser.flush()
	result = []
	time.sleep(1)
	while ser.inWaiting() > 0:
		s = ser.readline()
		result.append (s.strip())
		time.sleep(0.1)

	return result

def getMeasurments():
	rawMeasurments = "".join(command ('m'))
	m = re.match("(.*):(.*):(.*):(.*):(.*)", rawMeasurments)
	if m is not None:
		return (m.group(1), m.group(2), m.group(5))
	else:
		return None

if __name__ == '__main__':
	print(command('t'))
