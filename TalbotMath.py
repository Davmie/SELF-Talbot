from math import cos, pi, sqrt, sin

from scipy.integrate import quad


class TalbotMath:
    def __init__(self, p, mode, n, b=None):
        # mode - режим работы: 0 - округлая решётка, 1 - прямая решётка
        # При прямой решётки требуется b

        self.mode = mode

        self.p = p
        self.b = b
        self.n = n

        self.l = 5 * 10 ** (-7)

        self.omega = (2 * pi) / self.p
        self.k = (2 * pi) / self.l
        self.integrals = [(0, 0) for _ in range(-self.n, self.n + 1)]
        self.count_integrals()

    def I(self, x, z):
        sum_r = 0
        sum_i = 0
        for i in range(-self.n, self.n + 1):
            omega_n = i * self.omega
            arg = omega_n * x + sqrt(self.k * self.k - omega_n * omega_n) * z
            sum_r += self.fr(i, arg)
            sum_i += self.fi(i, arg)

        return sum_r * sum_r + sum_i * sum_i

    def fr(self, i, arg):
        return self.integrals[i][0] * cos(arg) - self.integrals[i][1] * sin(arg)

    def fi(self, i, arg):
        return self.integrals[i][1] * cos(arg) + self.integrals[i][0] * sin(arg)

    def fn_r(self, omega_n):
        return 1.0 / self.p * quad(
            lambda x: self.f0(x) * (cos(omega_n * x)), -self.p / 2, self.p / 2)[0]

    def fn_i(self, omega_n):
        return 1.0 / self.p * quad(
            lambda x: self.f0(x) * (-(sin(omega_n * x))), -self.p / 2, self.p / 2)[0]

    def count_integrals(self):
        for i in range(-self.n, self.n + 1):
            omega_n = i * self.omega
            self.integrals[i] = (self.fn_r(omega_n), self.fn_i(omega_n))

    def f0(self, x):
        coef = 2 * pi * x / self.p
        return 1.0 / 2 * (1 + cos(coef)) \
            if not self.mode else self.F(cos(coef) - cos(pi * (self.b / self.p)))

    @staticmethod
    def F(x):
        if x < 0:
            return 0
        if x == 0:
            return 1.0 / 2
        return 1
