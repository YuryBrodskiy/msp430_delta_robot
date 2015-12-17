import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
from matplotlib import animation

sq3 = np.sqrt(3)


def minangle(t):
    absmin_angle = t[np.argmin(np.abs(t))]
    return absmin_angle


def solve_ipk(e, f, g):
    roots = 2 * np.arctan(np.roots([g - e, 2 * f, g + e]))
    return roots


def inverse(rb, rp, lu, ll, x):
    a = rb - rp * 2
    b = rp * 3 / sq3 - rb * sq3 / 2.0
    c = rp - rb / 2

    t1 = x[0] ** 2 + x[1] ** 2 + x[2] ** 2

    e = 2 * lu * (x[1] + a)
    f = 2 * x[2] * lu
    g = t1 + a ** 2 + lu ** 2 + 2 * x[1] * a - ll ** 2
    theta1 = minangle(solve_ipk(e, f, g))

    t2 = t1 + b ** 2 + c ** 2 + lu ** 2 - ll ** 2

    e = -lu * (sq3 * (x[0] + b) + x[1] + c)
    g = t2 + 2 * (x[0] * b + x[1] * c)
    theta2 = minangle(solve_ipk(e, f, g))

    e = lu * (sq3 * (x[0] - b) - x[1] - c)
    g = t2 + 2 * (-x[0] * b + x[1] * c)
    theta3 = minangle(solve_ipk(e, f, g))

    return np.array([-theta1, -theta2, -theta3])


def p2c(th, r):
    return np.array([r * np.cos(th), r * np.sin(th)])


class Robot:
    # todo: mathematical configuration check
    # todo: hinge check if angles are physically allowed
    def __init__(self, rb, rp, lu, ll, pw=None):
        self.base_radius = rb
        self.platform_radius = rp
        self.upper_arm_length = lu
        self.lower_arm_length = ll
        self.pgram_width = pw

        self._xyz = np.array([0, 0, -0.9])
        self._theta = inverse(rb, rp, lu, ll, self.xyz)  # todo, forward kinematics first

        self.arm_attach = np.array([-1 / 2, 1 / 6, 5 / 6]) * np.pi

    @property
    def xyz(self):
        return self._xyz

    @xyz.setter
    def xyz(self, xyz):
        xyz = np.asarray(xyz, dtype=np.float32)
        self._theta = inverse(self.base_radius,
                              self.platform_radius,
                              self.upper_arm_length,
                              self.lower_arm_length, xyz)
        self._xyz = xyz

    @property
    def theta(self):
        return self._theta

    @theta.setter
    def theta(self, theta):
        theta = np.asarray(theta, dtype=np.float32)
        # todo: check config is possible
        # todo: forward kinematics
        self._theta = theta

    def act_coord(self, n):
        return np.append(p2c(self.arm_attach[n], self.base_radius), [0])

    def shoulder_hinge_coord(self, n):
        ludx, ludy = p2c(self._theta[n], self.upper_arm_length)
        return np.append(p2c(self.arm_attach[n], self.base_radius + ludx), [ludy])

    def platform_hinge_coord(self, n):
        return np.append(p2c(self.arm_attach[n], self.platform_radius) + self._xyz[0:2], self._xyz[2])

    def upper_arm_coord(self, n):
        base_coord = self.act_coord(n)
        hinge_coord = self.shoulder_hinge_coord(n)

        return np.vstack((base_coord, hinge_coord))

    def lower_arm_coord(self, n):
        shoulder_hinge_coord = self.shoulder_hinge_coord(n)
        platform_hinge_coord = self.platform_hinge_coord(n)

        return np.vstack((shoulder_hinge_coord, platform_hinge_coord))

    def prlgram_arm_coord(self, n):
        v1 = p2c(self.arm_attach[n]+np.pi/2, self.pgram_width/2)
        v2 = p2c(self.arm_attach[n]-np.pi/2, self.pgram_width/2)

        lower_arm_coord = self.lower_arm_coord(n)

        prlgram1 = np.copy(lower_arm_coord)
        prlgram2 = np.copy(lower_arm_coord)

        prlgram1[:, 0:2] += np.vstack((v1, v1))
        prlgram2[:, 0:2] += np.vstack((v2, v2))

        return np.vstack((prlgram1, prlgram2))


def visualize(robot, setp):
    if setp.ndim == 1:
        n_frames = 1
        setp = np.array([setp])
    else:
        n_frames = setp.shape[0]

    fig = plt.figure("config")

    # color:   blue       green      fuchsia
    colors = ('b', 'g', 'r')

    ax = fig.add_subplot(111, projection='3d')
    ax.auto_scale_xyz([-0.75, 0.75], [-0.75, 0.75], [-1.5, 0])
    ax.set_aspect("equal")

    ax.set_xlabel('X')
    ax.set_ylabel('Y')
    ax.set_zlabel('Z')

    circle_points = np.linspace(0, 2 * np.pi, num=100, endpoint=True)
    base_radius = robot.base_radius

    base_coord = np.column_stack((base_radius * np.cos(circle_points),
                                  base_radius * np.sin(circle_points),
                                  np.full(100, 0)))

    platform_radius = robot.platform_radius

    base, = ax.plot([], [], [], '-', color='k')
    platform, = ax.plot([], [], [], '-', color='k')
    upper_arm = sum([ax.plot([], [], [], '-', color=c) for c in colors], [])
    prlgram1 = sum([ax.plot([], [], [], '-', color=c) for c in colors], [])
    prlgram2 = sum([ax.plot([], [], [], '-', color=c) for c in colors], [])

    def init():

        base.set_data([], [])
        base.set_3d_properties([])

        platform.set_data([], [])
        platform.set_3d_properties([])

        for i in range(len(upper_arm)):
            upper_arm[i].set_data([], [])
            upper_arm[i].set_3d_properties([])

        for i in range(len(prlgram1)):
            prlgram1[i].set_data([], [])
            prlgram1[i].set_3d_properties([])

            prlgram2[i].set_data([], [])
            prlgram2[i].set_3d_properties([])

        return [base] + [platform] + upper_arm + prlgram1 + prlgram2

    def animate(i):

        robot.xyz = setp[i, ]

        base.set_data(base_coord[:, 0], base_coord[:, 1])
        base.set_3d_properties(base_coord[:, 2])

        platform_coord = np.column_stack((platform_radius * np.cos(circle_points),
                                          platform_radius * np.sin(circle_points),
                                          np.full(100, setp[i, 2])))

        platform.set_data(platform_coord[:, 0] + setp[i, 0], platform_coord[:, 1] + setp[i, 1])
        platform.set_3d_properties(platform_coord[:, 2])

        for i in range(len(upper_arm)):
            upper_arm_coord = robot.upper_arm_coord(i)
            upper_arm[i].set_data(upper_arm_coord[:, 0], upper_arm_coord[:, 1])
            upper_arm[i].set_3d_properties(upper_arm_coord[:, 2])

        for i in range(len(prlgram1)):
            prlgram_coord = robot.prlgram_arm_coord(i)

            prlgram1[i].set_data(prlgram_coord[0:2, 0], prlgram_coord[0:2, 1])
            prlgram1[i].set_3d_properties(prlgram_coord[0:2, 2])

            prlgram2[i].set_data(prlgram_coord[2:4, 0], prlgram_coord[2:4, 1])
            prlgram2[i].set_3d_properties(prlgram_coord[2:4, 2])

        return [base] + [platform] + upper_arm + prlgram1 + prlgram2

    if n_frames == 1:
        animate(0)
    else:
        ani = animation.FuncAnimation(fig, animate, frames=n_frames, blit=True, init_func=init, interval=50,
                                      repeat=True)

    plt.show()


rbot = Robot(0.164, 0.044, 0.524, 1.244, pw=0.131)

steps = np.linspace(0, 2 * np.pi, num=50, endpoint=False)

setpoint = np.column_stack((0.3 * np.cos(steps),
                            0.3 * np.sin(steps),
                            0.1 * np.sin(2 * steps) - 1.1))

visualize(rbot, setpoint)
