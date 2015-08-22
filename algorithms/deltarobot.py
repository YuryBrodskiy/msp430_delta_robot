__author__ = 'meinko'

# Very quick n dirty method to see resolution. Using calculation method from
# https://www.marginallyclever.com/other/samples/fk-ik-test.html

import math
import numpy as np
from mpl_toolkits.mplot3d import Axes3D
import matplotlib.pyplot as plt

e = 15.0  # end effector radius
f = 40.0  # base radius
re = 120.0  # parallelogram length
rf = 30.0  # upper joint length
bl = -100.0  # 'base level' (distance to actuator)
sr = 0.5  # servo resolution in degrees. (Hitec HS-A5076HB)


def cartesian(arrays, out=None):
    # copied from http://stackoverflow.com/questions/1208118/
    # using-numpy-to-build-an-array-of-all-combinations-of-two-arrays
    arrays = [np.asarray(x) for x in arrays]
    dtype = arrays[0].dtype

    n = np.prod([x.size for x in arrays])
    if out is None:
        out = np.zeros([n, len(arrays)], dtype=dtype)

    m = n / arrays[0].size
    out[:, 0] = np.repeat(arrays[0], m)
    if arrays[1:]:
        cartesian(arrays[1:], out=out[0:m, 1:])
        for j in range(1, arrays[0].size):
            out[j * m:(j + 1) * m, 1:] = out[0:m, 1:]
    return out


def forward_kinematics(upper_joint_angle):
    t = (f - e) * (1 / math.sqrt(3)) / 2
    dtr = math.pi / 180.0

    # convert to radians
    upper_joint_angle[0] *= dtr
    upper_joint_angle[1] *= dtr
    upper_joint_angle[2] *= dtr

    y1 = -(t + rf * math.cos(upper_joint_angle[0]))
    z1 = -rf * math.sin(upper_joint_angle[0])

    y2 = (t + rf * math.cos(upper_joint_angle[1])) * 0.5
    x2 = y2 * math.sqrt(3)
    z2 = -rf * math.sin(upper_joint_angle[1])

    y3 = (t + rf * math.cos(upper_joint_angle[2])) * 0.5
    x3 = -y3 * math.sqrt(3)
    z3 = -rf * math.sin(upper_joint_angle[2])

    dnm = (y2 - y1) * x3 - (y3 - y1) * x2

    w1 = y1 * y1 + z1 * z1
    w2 = x2 * x2 + y2 * y2 + z2 * z2
    w3 = x3 * x3 + y3 * y3 + z3 * z3

    # x = (a1*z + b1)/dnm
    a1 = (z2 - z1) * (y3 - y1) - (z3 - z1) * (y2 - y1)
    b1 = -((w2 - w1) * (y3 - y1) - (w3 - w1) * (y2 - y1)) / 2.0

    # y = (a2*z + b2)/dnm;
    a2 = -(z2 - z1) * x3 + (z3 - z1) * x2
    b2 = ((w2 - w1) * x3 - (w3 - w1) * x2) / 2.0

    # a*z^2 + b*z + c = 0
    a = a1 * a1 + a2 * a2 + dnm * dnm
    b = 2 * (a1 * b1 + a2 * (b2 - y1 * dnm) - z1 * dnm * dnm)
    c = (b2 - y1 * dnm) * (b2 - y1 * dnm) + b1 * b1 + dnm * dnm * (z1 * z1 - re * re)

    # discriminant
    d = b * b - 4.0 * a * c

    if d < 0:
        print("impossible config")
        return np.array([np.nan, np.nan, np.nan])
    else:
        z0 = -0.5 * (b + math.sqrt(d)) / a
        x0 = (a1 * z0 + b1) / dnm
        y0 = (a2 * z0 + b2) / dnm

        # print("x: {0:6.2f}  y: {1:6.2f}  z: {2:6.2f}".format(x0, y0, z0))
        return np.array([x0, y0, z0])


def calc_angle_yz(x0, y0, z0):
    y1 = -0.5 * 0.57735 * f  # f/2 * tg 30
    y0 -= 0.5 * 0.57735 * e  # shift center to edge
    # z = a + b*y
    a = (x0 * x0 + y0 * y0 + z0 * z0 + rf * rf - re * re - y1 * y1) / (2.0 * z0)
    b = (y1 - y0) / z0
    d = -(a + b * y1) * (a + b * y1) + rf * (b * b * rf + rf)

    if d < 0:
        return False
    else:
        yj = (y1 - a * b - math.sqrt(d)) / (b * b + 1)
        zj = a + b * yj
        return 180.0 * math.atan(-zj / (y1 - yj)) / math.pi + (180.0 if yj > y1 else 0.0)


def inverse_kinematics(effector_pos):
    theta1 = calc_angle_yz(effector_pos[0], effector_pos[1], effector_pos[2])

    theta2 = calc_angle_yz(effector_pos[0] * -0.5 + effector_pos[1] * (math.sqrt(3) / 2.0),
                           effector_pos[1] * -0.5 - effector_pos[0] * (math.sqrt(3) / 2.0), effector_pos[2])

    theta3 = calc_angle_yz(effector_pos[0] * -0.5 - effector_pos[1] * (math.sqrt(3) / 2.0),
                           effector_pos[1] * -0.5 + effector_pos[0] * (math.sqrt(3) / 2.0), effector_pos[2])

    if theta1 and theta2 and theta3:
        # print("theta 1: {0:5.2f}   theta 2: {1:5.2f}   theta 3: {2:5.2f}".format(theta1, theta2, theta3))
        return np.array([theta1, theta2, theta3])
    else:
        print("impossible config")
        return np.array([np.nan, np.nan, np.nan])


# spatial resolution

def resolution(effector_pos):
    theta = inverse_kinematics(effector_pos)

    loc = cartesian(([1., 0., -1.], [1., 0., -1.], [1., 0., -1.]))

    sloc = np.sum(loc, axis=1)

    loc = loc[np.abs(sloc) < 1, :]

    loc *= sr

    dpos = np.apply_along_axis(lambda da: forward_kinematics(theta + da), axis=1, arr=loc)

    fig = plt.figure()
    ax = fig.gca(projection='3d')

    ax.scatter(dpos[:, 0], dpos[:, 1], dpos[:, 2], c='r', marker='o')
    ax.scatter(effector_pos[0], effector_pos[1], effector_pos[2], s=60, c='g', marker='o')

    # Create cubic bounding box to simulate equal aspect ratio, http://stackoverflow.com/questions/
    # 13685386/matplotlib-equal-unit-length-with-equal-aspect-ratio-z-axis-is-not-equal-to
    max_range = np.array([dpos[:, 0].max() - dpos[:, 0].min(), dpos[:, 1].max() - dpos[:, 1].min(),
                          dpos[:, 2].max() - dpos[:, 2].min()]).max()
    Xb = 0.5 * max_range * np.mgrid[-1:2:2, -1:2:2, -1:2:2][0].flatten() + 0.5 * (dpos[:, 0].max() + dpos[:, 0].min())
    Yb = 0.5 * max_range * np.mgrid[-1:2:2, -1:2:2, -1:2:2][1].flatten() + 0.5 * (dpos[:, 1].max() + dpos[:, 1].min())
    Zb = 0.5 * max_range * np.mgrid[-1:2:2, -1:2:2, -1:2:2][2].flatten() + 0.5 * (dpos[:, 2].max() + dpos[:, 2].min())
    # Comment or uncomment following both lines to test the fake bounding box:
    for xb, yb, zb in zip(Xb, Yb, Zb):
        ax.plot([xb], [yb], [zb], 'w')

    ax.set_xlabel('X mm')
    ax.set_ylabel('Y mm')
    ax.set_zlabel('Z mm')

    ax.set_aspect('equal')

    plt.draw()

    # return np.apply_along_axis(lambda dp: np.linalg.norm(dp - effector_pos), axis=1, arr=dpos)
    return dpos[:, 2]

s = 70
b = -90


res = resolution(np.array([0, 0, b])) - b
print(res)

res = resolution(np.array([s, s, b])) - b
print(res)

res = resolution(np.array([s, -s, b])) - b
print(res)

res = resolution(np.array([-s, -s, b])) - b
print(res)

res = resolution(np.array([-s, s, b])) - b
print(res)


plt.show()