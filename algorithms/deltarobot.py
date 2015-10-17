

def inverse_kinematics(rb, rp, lu, ll):
    import numpy as np

    sq3 = np.sqrt(3)

    def inverse(x, y, z):
        a = rb - rp*2
        b = rp*3/sq3 - rb*sq3/2.0
        c = rp - rb/2

        t1 = np.dot([x, y, z], [x, y, z])

        e = 2*lu*(y + a)
        f = 2*z*lu
        g = t1 + a**2 + lu**2 + 2*y*a - ll**2
        theta1 = 2*np.arctan(np.roots([g-e, 2*f, g+e]))

        t2 = t1 + b**2 + c**2 + lu**2 - ll**2

        e = -lu*(sq3*(x + b) + y + c)
        g = t2 + 2*(x*b + y*c)
        theta2 = 2*np.arctan(np.roots([g-e, 2*f, g+e]))

        e = lu*(sq3*(x - b) - y - c)
        g = t2 + 2*(-x*b + y*c)
        theta3 = 2*np.arctan(np.roots([g-e, 2*f, g+e]))

        return np.array([theta1, theta2, theta3])

    return inverse


def plot_config(rb, rp, lu, ll):
    import numpy as np
    import matplotlib.pyplot as plt

    config = inverse_kinematics(rb, rp, lu, ll)

    def plot(x, y, z):
        theta = config(x, y, z)
        plt.plot([1,2,3,4])
        plt.ylabel('some numbers')
        plt.show()

    return plot






rbot = plot_config(0.164, 0.022, 0.524, 1.244)
rbot(0.00, 0.00, -0.9)
