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
    message = "[ %4.4f , %4.4f , %4.4f ]"% (num,num,num)
    print(message)
    ser.write(message)


#poss = [10,9]
#while 1==1:
#    for  pos in xrange(0,180):
#        print("Angle is %4.4f" % (pos))
#        testServo1(pos*math.pi/180.0)
#        time.sleep(1.0)
import math
ser.flushInput() 
ser.flushOutput()  
#message = "[ %4.4f , %4.4f , %4.4f ]"% (pos,pos,pos)
ser.write("[ 990 ,990 ,990  ]")
time.sleep(1.0)
ser.flushInput() 
ser.flushOutput()  
ser.write("[ 1500 ,1500 ,1500  ]")

while 1==1:
    for  x in xrange(0,50):
        ser.flushInput() 
        ser.flushOutput()  
        t=2*math.pi*x/50.0;
        x1 = math.sin(t)*150+1500
        x2 = math.sin(t+2*math.pi/3)*150+1500
        x3 = math.sin(t-2*math.pi/3)*150+1500
        message = "[ %4.1f , %4.1f , %4.1f ]"% (x1,x2,x3)
        #print(message)
        ser.write(message)
        time.sleep(0.1)
ser.close()

