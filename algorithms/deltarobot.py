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

    t1 = np.dot(x, x)

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

    return np.array([theta1, theta2, theta3])


class Robot:
    def __init__(self, rb, rp, lu, ll):
        self.base_radius = rb
        self.platform_radius = rp
        self.upper_arm_length = lu
        self.lower_arm_length = ll

        self._xyz = np.array([0, 0, -0.9])
        self._theta = inverse(rb, rp, lu, ll, self.xyz)  # todo, forward kinematics first

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


def visualize(robot):
    fig = plt.figure("config")

    ax = fig.add_subplot(111, projection='3d')
    ax.auto_scale_xyz([-0.75, 0.75], [-0.75, 0.75], [-1.5, 0])
    ax.set_aspect("equal")

    def init():
        pass

    def animate():
        pass


rbot = Robot(0.164, 0.022, 0.524, 1.244)
rbot.xyz = (0, 0, -1)
print(rbot.theta)
#
# def plot_config(rb, rp, lu, ll):
#     fig = plt.figure("config")
#
#     ax = fig.add_subplot(111, projection='3d')
#     ax.set_xlabel('X m')
#     ax.set_ylabel('Y m')
#     ax.set_zlabel('Z m')
#     ax.auto_scale_xyz([-0.75, 0.75], [-0.75, 0.75], [-1.5, 0])
#     ax.set_aspect("equal")
#
#     config = inverse_kinematics(rb, rp, lu, ll)
#
#     c_point = np.linspace(0, 2 * np.pi, num=100, endpoint=True)
#
#     base_points = np.array([rb * np.cos(c_point), rb * np.sin(c_point)])
#
#     base_config = np.array([-1 / 2, 1 / 6, -7 / 6]) * np.pi
#
#     def platform(x, y, z):
#         cx_platform = rp * np.cos(c_point) + x
#         cy_platform = rp * np.sin(c_point) + y
#         cz_platform = np.empty(100)
#         cz_platform.fill(z)
#
#         return np.array([cx_platform, cy_platform, cz_platform])
#
#     def arms(theta, x, y, z, config):
#         ludx, ludy = p2c(theta, lu)
#
#         lup = np.vstack((np.append(p2c(config, rb), [0]),
#                          np.append(p2c(config, rb + ludx), [ludy])))
#
#         llp = np.vstack((np.append(p2c(config, rp) + np.array([x, y]), z),
#                          np.append(p2c(config, rb + ludx), [ludy])))
#
#         return lup, llp
#
#     def draw_bot(i, xa, ya, za):
#         x = xa[i]
#         y = ya[i]
#         z = za[i]
#         theta = -config(x, y, z)
#
#         draw_parts = []
#
#         base_plot, = ax.plot(base_points[0, :], base_points[1, :])
#         draw_parts.append(base_plot)
#
#         platform_points = platform(x, y, z)
#         platform_plot, = ax.plot(platform_points[0, :], platform_points[1, :], platform_points[2, :])
#         draw_parts.append(platform_plot)
#
#         for i in range(len(base_config)):
#             lup, llp = arms(theta[i], x, y, z, base_config[i])
#             upper_arm_plot, = ax.plot(lup[:, 0], lup[:, 1], lup[:, 2])
#             lower_arm_plot, = ax.plot(llp[:, 0], llp[:, 1], llp[:, 2])
#             draw_parts.append(upper_arm_plot)
#             draw_parts.append(lower_arm_plot)
#
#         ax.auto_scale_xyz([-0.75, 0.75], [-0.75, 0.75], [-1.5, 0])
#         ax.set_aspect("equal")
#
#         draw_parts = tuple(draw_parts)
#
#         return draw_parts
#
#     def p2c(th, r):
#         return np.array([np.cos(th), np.sin(th)]) * r
#
#     def plot(x, y, z):
#         if len(x) == 1:
#             draw_bot(1, x, y, z)
#         else:
#             anim = animation.FuncAnimation(fig, draw_bot, fargs=(x, y, z), frames=100, interval=20, blit=True)
#         plt.show()
#
#     return plot
#
#
# rbot = plot_config(0.164, 0.022, 0.524, 1.244)
#
# move_points = np.linspace(0, 2 * np.pi, num=100, endpoint=True)
#
# x_move = 0.3 * np.cos(move_points)
# y_move = 0.3 * np.sin(move_points)
# z_move = 0.1 * np.sin(2*move_points) - 1
#
# rbot(x_move, y_move, z_move)
