import serial
import time


def command(cmd):
	ser = serial.Serial('/dev/rfcomm0', baudrate=115200)
	ser.timeout = 2
	ser.write(cmd)
	ser.flush()
	result = []
	time.sleep(1)
	while ser.inWaiting() > 0:
		s = ser.readline()
		result.append (s)
		time.sleep(0.1)

	return result

def getMeasurmetns():
	return (1,2,3.)

if __name__ == "__main__":
	print command('t')
