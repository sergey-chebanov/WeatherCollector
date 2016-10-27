import serial
import io
ser = serial.Serial('/dev/rfcomm0', timeout=1)
sio = io.TextIOWrapper(io.BufferedRWPair(ser, ser))

sio.write('m')
sio.flush() # it is buffering. required to get the data out *now*
hello = sio.readline()
print(hello)
