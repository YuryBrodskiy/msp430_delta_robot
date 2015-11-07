import serial
import random
import math
import time
# you will need the name of your serial port
# check in wiring - tools - menu
ser = serial.Serial('/dev/tty.uart-28FF467AF9D1272C', 9600)
#ser = serial.Serial('/dev/tty.uart-C2FF518F410F1D47', 9600)
def testRandom():
 
    ser.flushInput() 
    ser.flushOutput()  
    message = "[%2.2f,%2.2f,%2.2f]"% (random.random()*math.pi,random.random()*math.pi,random.random()*math.pi)
    print(message)
    ser.write(message)
    ser.close()

def testZero():
    ser.flushInput() 
    ser.flushOutput()  
    message = "[%2.2f,%2.2f,%2.2f]"% (0.0,0.0,0.0)
    print(message)
    ser.write(message)
def testServo1(num):
    ser.flushInput() 
    ser.flushOutput()  
    message = "[ %4.4f , %4.4f , %4.4f ]"% (num,1.0,1.0)
    print(message)
    ser.write(message)


poss = [10,9]

for  pos in xrange(0,180):
    print("Angle is %4.4f" % (pos))
    testServo1(pos*math.pi/180.0)
    time.sleep(0.5)

ser.close()

