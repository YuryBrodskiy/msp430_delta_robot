
import numpy as np

# solve for which points x y z the following holds:
# (x - s1[0])^2 + (y - s1[1])^2 (z - s1[2])^2 = r[0]^2
# (x - s2[0])^2 + (y - s2[1])^2 (z - s2[2])^2 = r[1]^2
# (x - s3[0])^2 + (y - s3[1])^2 (z - s3[2])^2 = r[2]^2


def intersect_point(s1, s2, s3, r):

    if s1[2] == s2[2] == s3[2]:
        a = 2*(s3[0] - s1[0])
        b = 2*(s3[1] - s1[1])
        c = r[0]**2 - r[2]**2 - s1[0]**2 - s1[1]**2 + s3[0]**2 + s3[1]**2
        d = 2*(s3[0] - s2[0])
        e = 2*(s3[1] - s2[1])
        f = r[1]**2 - r[2]**2 - s2[0]**2 - s2[1]**2 + s3[0]**2 + s3[1]**2

        t1 = (a*e - b*d)

        x = (c*e - b*f) / t1
        y = (a*f - c*d) / t1

        da = 1
        db = -2*s1[2]
        dc = s1[2]**2 - r[0]**2 + (x - s1[0])**2 + (y - s1[1])**2

        z = np.roots([da, db, dc])

        return np.array([x, x]), np.array([y, y]), z

    else:
        d31 = s3 - s1
        d32 = s3 - s2

        n1 = np.dot(s1, s1)
        n2 = np.dot(s2, s2)
        n3 = np.dot(s3, s3)

        q = r[0]**2 - r[2]**2 - n1 + n3
        p = r[1]**2 - r[2]**2 - n2 + n3

        t1 = d31[0]*d32[2] - d31[2]*d32[0]
        t2 = 2*d32[2]

        a4 = (d31[2]*d32[1] - d31[1]*d32[2]) / t1
        a5 = -(d31[2]*p - d32[2]*q) / (2*t1)
        a6 = (-2*d32[0]*a4 - 2*d32[1]) / t2
        a7 = (p - 2*d32[0]*a5) / t2

        a = a4**2 + 1 + a6**2
        b = 2*a4*(a5 - s1[0]) - 2*s1[1] + 2*a6*(a7 - s1[2])
        c = a5*(a5 - 2*s1[0]) + a7*(a7 - 2*s1[2]) + n1 - r[0]**2

        y = np.roots([a, b, c])
        x = a4*y+a5
        z = a6*y+a7

        return x, y, z


c1 = np.array([0, 0, 0])
c2 = np.array([3, 0, 0])
c3 = np.array([1, -3, 0])

r = np.array([np.sqrt(2), np.sqrt(5), 3])

ret = intersect_point(c1, c2, c3, r)
print(ret)