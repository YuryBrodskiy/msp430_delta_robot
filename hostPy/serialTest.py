from DeltaDriver import DeltaDriver 
from DeltaRobot import DeltaRobot
import time
import math

def main():
    print "start moving the robot"
    robot = DeltaRobot(20,30,40,160)
    with DeltaDriver('',[0,0,0],[90,90,90],[900,900,900],[1800,1800,1800]) as delta:
        delta.calibrate([0,0,150])
#        for x in range(10,50):
#            time.sleep(0.5)
#            print x
#            delta.setAngles([x,x,x])
        for  x in xrange(0,50):
            t= 2*math.pi*x/50.0;
            x = int(math.sin(t)*60.0)
            y = int(math.cos(t)*60.0)
            cartPos= [x,y,-180.0]
            jointPos = robot.inverse(cartPos)
            print cartPos
            print jointPos
            time.sleep(0.5)
            delta.setAngles(jointPos)
        


if __name__ == "__main__":
    main()

