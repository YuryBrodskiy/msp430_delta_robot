from DeltaDriver import DeltaDriver 
from DeltaRobot import DeltaRobot
import time
import math

def main():
    print "start moving the robot"
    robot = DeltaRobot(20,30,40,160)
    with DeltaDriver('',[0,0,0],[90,90,90],[900,900,900],[1800,1800,1800]) as delta:
        delta.calibrate([ 0,-100,170])
        # for x in range(10,80):
        #    time.sleep(0.5)
        #    print x
        #    delta.setAngles([x,x,x])
        
        # for x in range(1,800):
   #         time.sleep(0.01)
   #         print x
   #         x=x/10.0+10.0;
   #         delta.setAngles([x,x,x])
        # for  x in xrange(0,1500):
        #     t= 2*math.pi*x/20.0;
        #     x = int(math.cos(t)*30.0)
        #     y = int(math.cos(t)*30.0)
        #     cartPos= [x,y,-155.0]
        #     jointPos = robot.inverse(cartPos)
        #     #print cartPos
        #     #print jointPos
        #     time.sleep(0.05)
        #     delta.setAngles(jointPos)
        x = 60.0
        y = 60.0
        for  t in xrange(0,500):
            x*=-1
            y*=-1
            
            cartPos= [x,y,-150.0]
            jointPos = robot.inverse(cartPos)
            print cartPos
            print jointPos
            time.sleep(2)
            delta.setAngles(jointPos)
 #


if __name__ == "__main__":
    main()

import numpy as np

    
class DeltaRobot:
    def __init__(self, end_effector, base,bicep_length, forearm_length):
        self.end_effector = end_effector;            
        self.base = base;            
        self.bicep_length = bicep_length;
        self.forearm_length = forearm_length;
    def inverse(self,cartPos):
        sqrt3  = np.float(np.sqrt(3.0));
        sin120 = sqrt3/2.0;
        cos120 = -0.5;
        result = [ 0, 0, 0];
        x=cartPos[0];
        y=cartPos[1];
        z=cartPos[2];
        result[0] = 90.0 - self.delta_calcAngleYZ(                   x,                 y, z);
        result[1] = 90.0 - self.delta_calcAngleYZ( x*cos120 + y*sin120, y*cos120-x*sin120, z);#  // rotate coords to +120 deg;
        result[2] = 90.0 - self.delta_calcAngleYZ( x*cos120 - y*sin120, y*cos120+x*sin120, z);# // rotate coords to -120 deg
        return result;
    def delta_calcAngleYZ(self,x0,y0,z0):
        e = self.end_effector;            
        f = self.base ;   
        rf = self.bicep_length;
        re = self.forearm_length;
        y1 = -0.5 * 0.57735 * f; # f/2 * tg 30
        y0 = y0 - 0.5 * 0.57735 * e;  # shift center to edge
        #  z = a + b*y
        a = (x0*x0 + y0*y0 + z0*z0 +rf*rf - re*re - y1*y1)/(2.0*z0);
        b = (y1-y0)/z0;
        # discriminant
        d = -(a+b*y1)*(a+b*y1)+rf*(b*b*rf+rf); 
        if d < 0: 
            result = [];#  non-existing povar.  return error, theta
        else:
            yj = (y1 - a*b - np.sqrt(d))/(b*b + 1); # choosing outer povar
            zj = a + b*yj;
            if (yj>y1):
                tmp= 180.0;
            else:
                tmp = 0.0;
            result = np.float(np.arctan(-zj/(y1 - yj)) * 180.0/np.pi + (tmp));
        return result;  
