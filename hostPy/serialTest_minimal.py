import serial
import random
import math
import time
# you will need the name of your serial port
# check in wiring - tools - menu

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
    ser = serial.Serial('/dev/tty.uart-28FF467AF9D1272C', 9600)
    ser.flushInput() 
    ser.flushOutput()  

    ser.write(makeMessage([ 990 ,990 ,990  ]))
    ser.close()
    
def main():
    ser = serial.Serial('/dev/tty.uart-28FF467AF9D1272C', 9600)
    ser.flushInput() 
    ser.flushOutput()  

    ser.write(makeMessage([ 990 ,990 ,990  ]))
    time.sleep(1.0)
    ser.flushInput() 
    ser.flushOutput()  
    ser.write(makeMessage([ 1500 ,1500 ,1500  ]))

    while 1==1:
        for  x in xrange(0,50):
            ser.flushInput() 
            ser.flushOutput()  
            t=2*math.pi*x/50.0;
            x1 = int(math.sin(t)*150+1500)
            x2 = int(math.sin(t+2*math.pi/3)*150+1500)
            x3 = int(math.sin(t-2*math.pi/3)*150+1500)
            message = makeMessage([ x1,x2,x3])
            print(message)
            ser.write(message)
            time.sleep(0.1)
    ser.close()
if __name__ == "__main__":
    main()
