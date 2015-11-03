__author__ = 'yury'
import math
#import numpy as np

import bpy
import mathutils as bmath
class DHParams:
    def __init__(self, d, a,alpha,theta):
        self.d = d
        self.a = a 
        self.alpha = alpha
        self.theta = theta
    def getPose(self):
        d  = self.d;
        a  = self.a;
        cth = math.cos(self.theta);
        cal = math.cos(self.alpha);
        sth = math.sin(self.theta);
        sal = math.sin(self.alpha);
        return bmath.Matrix(
                 [[    cth,    -sth,    0,      a],
                  [sth*cal, cth*cal, -sal, -sal*d],
                  [sth*sal, cth*sal,  cal,  cal*d],
                  [     0,       0,    0,      1]])
        
class Joint:  
    def __init__(self, name, uTwist, dh):
        self.name   = name
        self.parent = []
        self.childs = []
        self.uTwist  = uTwist
def main():
    print(DHParams(0,0,0,0).getPose)

if __name__ =="__main__":
    main()