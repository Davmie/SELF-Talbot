#include "TalbotMath.h"

double TalbotMath::f(double x) const
{
    return F(cos(2 * M_PI * x / this->p) - cos(M_PI * this->b / this->p));
}

double TalbotMath::F(double x)
{
    if (x > 0)
        return 1;
    if (x < 0)
        return 0;
    else
        return 0.5;
}

double TalbotMath::fn(int n)
{
    return 1 / this->p * IntegralSimpson(- (this->p/ 2), this->p / 2, SUBDIVISION, n);
}

double TalbotMath::IntegralSimpson(double a,double b, int N, int n)
{
    double S = 0, x, h;
    h = (b - a)/N;
    x = a + h;
    while (x < b)
    {
        S += 4 * int_func(x, n);
        x += h;
        if (x >= b)
            break;
        S += 2 * int_func(x, n);
        x += h;
    }
    S += int_func(a, n) + int_func(b, n);
    S *= h / 3;
    return S;
}

double TalbotMath::int_func(double x, int n)
{
    return f(x) * exp(-i * (double(n) * ((2 * M_PI) / this->p) * x));
}

double TalbotMath::main_f(double x, int N)
{
    double sum = 0;

    for (int j = -N; j < N; j++)
        sum += fn(j) * exp(-i * (double(j) * ((2 * M_PI) / this->p) * x));

    return sum;
}
