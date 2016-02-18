import serial
import math
import time

from os import listdir
from os.path import join
import re
# you will need the name of your serial port
# check in wiring - tools - menu
class DeltaDriver:
    def __init__(self, portUrl, minAngle,maxAngle, minTime,maxTime):
        if portUrl == '':
            portUrl=getUARTUrl()
        self.port = serial.Serial(portUrl, 9600)
        self.msCorrection = [0,0,0]
        self.servo = []
        for i in range(3):
            self.servo.append(Servo(minAngle[i],maxAngle[i], minTime[i],maxTime[i]))
    def calibrate (self,val):
        self.msCorrection = val
    def setTimes(self,val):
        self.port.flushInput() 
        self.port.flushOutput() 
        x1 = val[0] + self.msCorrection[0]
        x2 = val[1] + self.msCorrection[1]
        x3 = val[2] + self.msCorrection[2]
        message = makeMessage([x1,x2,x3])
        self.port.write(message)
    def setAngles(self,val):
        self.setTimes([self.servo[i].getTime(val[i]) for i in range(3)])
    def __del__(self):
        self.port.close()
    def __enter__(self):
        return self
    def __exit__(self, exc_type, exc_value, traceback):
        pass
class Servo:
    def __init__(self, minAngle,maxAngle, minTime,maxTime):
        self.minAngle = minAngle;
        self.maxAngle = maxAngle;
        self.minTime = minTime;
        self.maxTime = maxTime;
    def getTime(self,angle):
        return  (self.maxTime-self.minTime)/(self.maxAngle-self.minAngle)*(angle-self.minAngle) +  self.minTime;
def makeMessageDigit(inputVal):
    lowBitMask = int(255)
    lowBit = (inputVal & lowBitMask)
    highBit = (inputVal>>8)
    return [highBit,lowBit]
def decodeMessageDigit(inputVal):
    highBit = inputVal[0]<<8
    lowBit = inputVal[1]
    return highBit + lowBit
def makeMessage(val):
    return makeMessageDigit(val[0])+makeMessageDigit(val[1])+makeMessageDigit(val[2])+makeMessageDigit(val[0]+val[1]+val[2])
def decodeMessage(message):
    return [decodeMessageDigit(message[0:2]),decodeMessageDigit(message[2:4]),decodeMessageDigit(message[4:6]),decodeMessageDigit(message[6:8])]
def getUARTUrl():
    allDevicesUrls =  listdir('/dev/')
    portUrls = [f for f in allDevicesUrls if re.match('tty\.uart.*', f)]
    return join('/dev/',portUrls[0])# will throw up if nothing found/ nice to check the system type

def test_Messages():
    print makeMessageDigit(0)
    print decodeMessageDigit(makeMessageDigit(0))
    print makeMessageDigit(255)
    print decodeMessageDigit(makeMessageDigit(255))
    print makeMessageDigit(256)
    print decodeMessageDigit(makeMessageDigit(256))
    print makeMessageDigit(257)
    print decodeMessageDigit(makeMessageDigit(257))
    print makeMessageDigit(258)+makeMessageDigit(258)
    print makeMessage([2000,2000,200])
    print decodeMessage(makeMessage([2000,2000,200]))
def test_com():
    ser = serial.Serial(getUARTUrl(), 9600)
    ser.flushInput() 
    ser.flushOutput()  

    ser.write(makeMessage([ 990 ,990 ,990  ]))
    ser.close()
def main():
    with DeltaDriver('',[0,0,0],[90,90,90],[900,900,900],[1800,1800,1800]) as delta:
        delta.setAngles([990, 990, 990])
        time.sleep(1.0)
        delta.setAngles([1500, 1500, 1500])
        while 1==1:
            for  x in xrange(0,50):
                t=2*math.pi*x/50.0;
                x1 = int(math.sin(t)*150+1500)
                x2 = int(math.sin(t+2*math.pi/3)*150+1500)
                x3 = int(math.sin(t-2*math.pi/3)*150+1500)
                message = makeMessage([ x1,x2,x3])
                print(message)
                print(decodeMessage(message))
                delta.setAngles(message)
                time.sleep(0.1)
if __name__ == "__main__":
    test_Messages()
    test_com()
    main()
