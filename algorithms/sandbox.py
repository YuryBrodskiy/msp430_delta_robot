import numpy as np


def inverse(E, F, RE, RF, X0, Y0, Z0):
    R3 = np.sqrt(3)

    E2 = E/2.0
    F2 = F/2.0
    E4 = E/4.0
    F4 = F/4.0

    C1X = X0
    C1Y = Y0-E2/R3
    C1Z = Z0

    C2X = X0+E4
    C2Y = Y0+E4/R3
    C2Z = Z0

    RF2 = RF**2

    C3X = X0-E4
    C3Y = C2Y
    C3Z = Z0

    D1Y = -F2/R3
    D2X = F4
    D2Y = F4/R3
    D3X = -F4
    D3Y = D2Y
    EF = RE**2-RF2

    X1 = C1X
    Y1 = C1Y-D1Y
    Z1 = C1Z
    W1 = (EF - C1X**2 + D1Y**2 - C1Y**2 - C1Z**2)/2.0

    X2 = C2X-D2X
    Y2 = C2Y-D2Y
    Z2 = C2Z
    W2 = (EF + D2X**2 - C2X**2 + D2Y**2 - C2Y**2 - C2Z**2)/2.0

    X3 = C3X - D3X
    Y3 = C3Y - D3Y
    Z3 = C3Z
    W3 = (EF + D3X**2 - C3X**2 + D3Y**2 - C3Y**2 - C3Z**2)/2.0

    P02 = Z1
    P03 = -Y1
    P23 = W1

    Q01 = -R3*Z2
    Q02 = -Z2
    Q03 = Y2 + R3*X2
    Q23 = -W2
    Q31 = R3*W2

    R01 = R3*Z3
    R02 = -Z3
    R03 = Y3-R3*X3
    R23 = -W3
    R31 = -R3*W3

    RD = 180.0/np.pi

    T = P02/P03
    U = P23/P03

    A = T*T+1
    B = T*(D1Y-U)
    C = U*(2*D1Y-U) - D1Y**2 + RF2
    D = B*B+A*C

    if D < 0:
        print('no solution')
        return
    else:
        D = np.sqrt(D)
        V1 = np.array(((B - D)/A, (B + D)/A))
        S = V1/RF
        theta1 = RD*np.arcsin(S)

    T = Q02/Q03
    U = Q01/Q03
    V = Q31/Q03
    W = Q23/Q03

    A = T*T + U*U + 1
    B = U*(D2X + V) + T*(D2Y - W)
    C = RF2 - D2X*(D2X + 2*V) - D2Y*(D2Y - 2*W) - V*V - W*W
    D = B*B + A*C

    if D < 0:
        print('no solution')
        return
    else:
        D = np.sqrt(D)
        V2 = np.array(((B - D)/A, (B + D)/A))
        S = V2/RF
        theta2 = RD*np.arcsin(S)

    T = R02/R03
    U = R01/R03
    V = R31/R03
    W = R23/R03

    A = T*T + U*U + 1
    B = U*(D3X + V) + T*(D3Y - W)
    C = RF2 - D3X*(D3X + 2*V) - D3Y * (D3Y - 2*W) - V*V - W*W
    D = B*B + A*C

    if D < 0:
        print('no solution')
        return
    else:
        D = np.sqrt(D)
        V3 = np.array(((B - D)/A, (B + D)/A))
        S = V3/RF
        theta3 = RD*np.arcsin(S)

    return np.array((theta1, theta2, theta3))

E = 8
F = 16
RE = 10.3094
RF = 8

X0 = 2
Y0 = 3
Z0 = -8.7488

print(inverse(E, F, RE, RF, X0, Y0, Z0))


E = 8
F = 16
RE = 10.3094
RF = 8

X0 = 3
Y0 = 2
Z0 = -8.7488

print(inverse(E, F, RE, RF, X0, Y0, Z0))


E = 0.076*2
F = 0.567
RE = 1.244
RF = 0.524

X0 = 0.0
Y0 = 0.0
Z0 = -0.9

print(inverse(E, F, RE, RF, X0, Y0, Z0))


E = 0.076*2
F = 0.567
RE = 1.244
RF = 0.524

X0 = 0.3
Y0 = 0.5
Z0 = -1.1

print(inverse(E, F, RE, RF, X0, Y0, Z0))