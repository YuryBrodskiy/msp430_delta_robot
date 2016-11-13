import numpy as np
import calc_helper as ch


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
        self._theta = ch.inverse(rb, rp, lu, ll, self.xyz)

        self.arm_attach = np.array([-1 / 2, 1 / 6, 5 / 6]) * np.pi

    @property
    def xyz(self):
        return self._xyz

    @xyz.setter
    def xyz(self, xyz):
        xyz = np.asarray(xyz, dtype=np.float32)

        theta = ch.inverse(self.base_radius,
                           self.platform_radius,
                           self.upper_arm_length,
                           self.lower_arm_length, xyz)

        # forward calc with theta, to check is given xyz is indeed possible, and we have a consistent configuration.
        xyz_check = ch.forward(self.base_radius,
                               self.platform_radius,
                               self.upper_arm_length,
                               self.lower_arm_length, theta)

        if np.allclose(xyz, xyz_check):
            self._theta = theta
            self._xyz = xyz
        else:
            print('This x,y and z coordinate does not resolve in a buildable configuration')

    @property
    def theta(self):
        return self._theta

    @theta.setter
    def theta(self, theta):
        theta = np.asarray(theta, dtype=np.float32)
        xyz = ch.forward(self.base_radius,
                         self.platform_radius,
                         self.upper_arm_length,
                         self.lower_arm_length, theta)

        # forward calc with theta, to check is given theta is indeed possible, and we have a consistent configuration.
        theta_check = ch.inverse(self.base_radius,
                                 self.platform_radius,
                                 self.upper_arm_length,
                                 self.lower_arm_length, xyz)

        if np.allclose(theta, theta_check):
            self._xyz = xyz
            self._theta = theta
        else:
            print('The upper arm angles do not resolve in a buildable configuration')


if __name__ == "__main__":
    print("Executing as main program")
    test = Robot(0.164, 0.044, 0.524, 1.244)
    test.xyz = (0, 0, -0.9)
    print(test.xyz)
    print(test.theta)
