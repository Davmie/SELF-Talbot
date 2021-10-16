from math import cos, pi, exp, sqrt, sin

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

    def I(self, x, z):
        sum_r = 0
        sum_i = 0
        for i in range(-self.n, self.n + 1):
            omega_n = i * self.omega
            sum_r += self.fr(x, z, omega_n)
            sum_i += self.fi(x, z, omega_n)
                   #exp((1j * (omega_n * x + sqrt(self.k ** 2 - omega_n ** 2) * z)).imag)

        return sum_r ** 2 + sum_i ** 2
    
    def fr(self, x, z, omega_n):
        return self.fn_r(omega_n) * cos(omega_n * x + sqrt(self.k ** 2 - omega_n ** 2) * z) - self.fn_i(omega_n) * sin(omega_n * x + sqrt(self.k ** 2 - omega_n ** 2) * z)
        
    def fi(self, x, z, omega_n):
        return  self.fn_i(omega_n) * cos(omega_n * x + sqrt(self.k ** 2 - omega_n ** 2) * z) + self.fn_r(omega_n) * sin(omega_n * x + sqrt(self.k ** 2 - omega_n ** 2) * z)

    def fn_r(self, omega_n):
        return 1.0 / self.p * quad(
            lambda x : self.f0(x) * (cos(omega_n * x)), -self.p / 2, self.p / 2)[0]

    def fn_i(self, omega_n):
        return 1.0 / self.p * quad(
            lambda x : self.f0(x) * (-(sin(omega_n * x))), -self.p / 2, self.p / 2)[0]

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
