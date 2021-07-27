def x_t(t):
    p1 = 0.002066
    p2 = -0.01468
    p3 = 0.001782
    x = p1 * t ** 2 + p2 * t + p3
    return x


def y_x(x):
    p1 = -697.6
    p2 = 8.882
    p3 = 0.02233
    p4 = -0.0001549
    y = p1 * x ** 3 + p2 * x ** 2 + p3 * x + p4
    return y


def theta_t(t):
    p1 = -2.157 * 10**-6
    p2 = 0.0004968
    p3 = -0.05614
    p4 = 2.721
    theta = p1 * t ** 3 + p2 * t ** 2 + p3 * t + p4
    return theta
