import serial
import random
import math
import time
# you will need the name of your serial port
# check in wiring - tools - menu
def testCorrectMessage(ser,t1,t2,t3):
    ser.flushInput() 
    ser.flushOutput()  
    message = "[ %4.4f , %4.4f , %4.4f ]"% (t1,t2,t3)
    print(message)
    ser.write([-1,t1,t2,t3,t1+t2+t3])

def testIncorrectMessageEnd(ser,t1,t2,t3):
    ser.flushInput() 
    ser.flushOutput()  
    message = "[ %4.4f , %4.4f , %4.4f ]"% (t1,t2,t3)
    print(message)
    ser.write([-1,t1,t2,t3,1+t1+t2+t3])

def testIncorrectMessageBegin(ser,t1,t2,t3):
    ser.flushInput() 
    ser.flushOutput()  
    message = "[ %4.4f , %4.4f , %4.4f ]"% (t1,t2,t3)
    print(message)
    ser.write([1,t1,t2,t3,t1+t2+t3])
def main():
    ser = serial.Serial('/dev/tty.uart-28FF467AF9D1272C', 9600)
    ser.write([1])
    ser.close()
def main1():
    ser = serial.Serial('/dev/tty.uart-28FF467AF9D1272C', 9600)
    print("corretTry")
    testCorrectMessage(ser,1000,2000,3000)
    time.sleep(3)
    print("wrong end")
    testIncorrectMessageEnd(ser,1000,2000,3000)
    time.sleep(3)
    print("wrong begin")
    testIncorrectMessageBegin(ser,1000,2000,3000)
    ser.close()

if __name__ == "__main__":
    main()
