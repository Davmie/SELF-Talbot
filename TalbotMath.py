from math import cos, pi, exp, sqrt, inf

from scipy.integrate import quad


class TalbotMath:
    def __init__(self, p, mode, n, b=None):
        # mode - режим работы: 0 - округлая решётка, 1 - прямая решётка
        # При прямой решётки требуется b

        self.mode = mode

        self.p = p
        self.b = b
        self.n = n

        self.l = 5 * 10 ** (-9)

        self.omega = (2 * pi) / self.p
        self.k = (2 * pi) / self.l

    def I(self, x, z):
        return (abs(self.f(x, z))) ** 2

    def f(self, x, z):
        sum = 0
        for i in range(-self.n, self.n + 1):
            omega_n = i * self.omega
            sum += self.fn(omega_n) * \
                   exp((1j * (omega_n * x + sqrt(self.k ** 2 - omega_n ** 2) * z)).imag)

            print(self.fn(omega_n))

        return sum

    def fn(self, omega_n):
        return 1.0 / self.p * quad(
            lambda x : self.f0(x) * exp((-1j * omega_n * x).imag), -self.p / 2, self.p / 2)[0]

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
