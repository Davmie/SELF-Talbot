from math import cos
from cmath import sqrt, pi, exp

from scipy.integrate import quad

# Библиотека с комплексным интегралом
# from quadpy import quad


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
        self.integrals = [0] * (self.n * 2 + 1)
        self.count_integrals()

    def I(self, x, z):
        return (abs(self.f(x, z))) ** 2

    def f(self, x, z):
        sum = 0
        for i in range(-self.n, self.n + 1):
            omega_n = i * self.omega
            sum += self.integrals[i] * \
                   exp(1j * (omega_n * x + sqrt(self.k ** 2 - omega_n ** 2) * z))

        return sum

    def fn(self, omega_n):
        real_integral = quad(
            lambda x: (self.f0(x) * exp(-1j * omega_n * x)).real, -self.p / 2, self.p / 2)
        imag_integral = quad(
            lambda x: (self.f0(x) * exp(-1j * omega_n * x)).imag, -self.p / 2, self.p / 2)

        return 1.0 / self.p * (real_integral[0] + 1j * imag_integral[0])

    def count_integrals(self):
        for i in range(-self.n, self.n + 1):
            omega_n = i * self.omega
            self.integrals[i] = self.fn(omega_n)

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
