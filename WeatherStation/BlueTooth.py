import bluetooth


btSocket = bluetooth.BluetoothSocket(bluetooth.RFCOMM)
btSocket.connect(('98:D3:31:20:6D:74', 1))
btSocket.send(b'm')
print(btSocket.read(1024))
