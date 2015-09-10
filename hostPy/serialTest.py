import serial
import random
import math
# you will need the name of your serial port
# check in wiring - tools - menu
#ser = serial.Serial('/dev/tty.uart-28FF467AF9D1272C', 9600)
ser = serial.Serial('/dev/tty.uart-C2FF518F410F1D47', 9600)

ser.flushInput() 
ser.flushOutput()  
message = "[%2.2f,%2.2f,%2.2f]"% (random.random()*math.pi,random.random()*math.pi,random.random()*math.pi)
print(message)
ser.write(message)

ser.close()