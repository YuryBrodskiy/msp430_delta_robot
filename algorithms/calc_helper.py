
import numpy as np

# inverse and forward calculations based on:
# http://forums.trossenrobotics.com/tutorials/introduction-129/delta-robot-kinematics-3276/

# trigonometric constants
sqrt3 = np.sqrt(3.0)
pi = np.pi
sin120 = sqrt3/2.0
cos120 = -0.5
tan60 = sqrt3
sin30 = 0.5
tan30 = 1/sqrt3
dtr = np.pi/180.0


def forward(rb, rp, rf, re, theta_deg):
    e = 2*sqrt3*rp
    f = 2*sqrt3*rb
    
    t = (f-e)*tan30/2

    theta = theta_deg * dtr

    y1 = -(t + rf*np.cos(theta[0]))
    z1 = -rf*np.sin(theta[0])

    y2 = (t + rf*np.cos(theta[1]))*sin30
    x2 = y2*tan60
    z2 = -rf*np.sin(theta[1])

    y3 = (t + rf*np.cos(theta[2]))*sin30
    x3 = -y3*tan60
    z3 = -rf*np.sin(theta[2])

    dnm = (y2-y1)*x3-(y3-y1)*x2

    w1 = y1*y1 + z1*z1
    w2 = x2*x2 + y2*y2 + z2*z2
    w3 = x3*x3 + y3*y3 + z3*z3

    # x = (a1*z + b1)/dnm
    a1 = (z2-z1)*(y3-y1)-(z3-z1)*(y2-y1)
    b1 = -((w2-w1)*(y3-y1)-(w3-w1)*(y2-y1))/2.0

    # y = (a2*z + b2)/dnm;
    a2 = -(z2-z1)*x3+(z3-z1)*x2
    b2 = ((w2-w1)*x3 - (w3-w1)*x2)/2.0

    # a*z^2 + b*z + c = 0
    a = a1*a1 + a2*a2 + dnm*dnm
    b = 2*(a1*b1 + a2*(b2-y1*dnm) - z1*dnm*dnm)
    c = (b2-y1*dnm)*(b2-y1*dnm) + b1*b1 + dnm*dnm*(z1*z1 - re*re)

    # discriminant
    d = b*b - 4.0*a*c
    if d < 0:
        print('we have an issue')
    else:
        z0 = -0.5*(b+np.sqrt(d))/a
        x0 = (a1*z0 + b1)/dnm
        y0 = (a2*z0 + b2)/dnm
        return np.array((x0, y0, z0))


def calc_angle_yz(e, f, re, rf, x0, y0, z0):
    y1 = -0.5 * tan30 * f  # f/2 * tg 30
    y0 -= 0.5 * tan30 * e  # shift center to edge

    # z = a + b*y
    a = (x0*x0 + y0*y0 + z0*z0 + rf*rf - re*re - y1*y1)/(2*z0)
    b = (y1-y0)/z0

    # discriminant
    d = -(a+b*y1)*(a+b*y1)+rf*(b*b*rf+rf)

    if d < 0:
        print('we have an issue')
    else:
        yj = (y1 - a*b - np.sqrt(d))/(b*b + 1)  # choosing outer point
        zj = a + b*yj

        if yj > y1:
            na = 180.0
        else:
            na = 0.0

        return 180.0*np.arctan(-zj/(y1 - yj))/np.pi + na


def inverse(rb, rp, rf, re, xyz):
    e = 2*sqrt3*rp
    f = 2*sqrt3*rb
    
    theta1 = calc_angle_yz(e, f, re, rf, xyz[0], xyz[1], xyz[2])
    theta2 = calc_angle_yz(e, f, re, rf, xyz[0]*cos120 + xyz[1]*sin120, xyz[1]*cos120 - xyz[0]*sin120, xyz[2])  # rotate coords to +120 deg
    theta3 = calc_angle_yz(e, f, re, rf, xyz[0]*cos120 - xyz[1]*sin120, xyz[1]*cos120 + xyz[0]*sin120, xyz[2])  # rotate coords to -120 deg
    
    return np.array((theta1, theta2, theta3))

    # e = 115.0
    # f = 457.3
    # re = 232.0
    # rf = 112.0

    #
    # E = 8
    # F = 16
    # RE = 10.3094
    # RF = 8
    #
    # X0 = 2
    # Y0 = 3
    # xyz[2] = -8.7488
    #
    # print(inverse(E, F, RE, RF, X0, Y0, Z0))
    #
    # E = 0.076*2
    # F = 0.567
    # RE = 1.244
    # RF = 0.524
    #
    # X0 = 0.0
    # Y0 = 0.0
    # Z0 = -0.9
    #
    # print(inverse(E, F, RE, RF, X0, Y0, Z0))
    #
    # E = 0.076*2
    # F = 0.567
    # RE = 1.244
    # RF = 0.524
    #
    # X0 = 0.3
    # Y0 = 0.5
    # Z0 = -1.1
    #
    # print(inverse(E, F, RE, RF, X0, Y0, Z0))