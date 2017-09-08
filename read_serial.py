import serial

ser = serial.Serial("/dev/tty.usbmodem41", timeout=0.1)
# ser = serial.Serial('/dev/ttyS0', timeout=0.1)
while(True):
    line = ser.readline()
    print("v" + line)
ser.close()
