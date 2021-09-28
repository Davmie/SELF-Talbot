#ifndef TALBOT_TALBOTMATH_H
#define TALBOT_TALBOTMATH_H

#include "cmath"

#define i (-1)
#define SUBDIVISION 1000

class TalbotMath
{
private:
    double b;
    double p;
    static double F(double x);
    double f(double x) const;
    double fn(int n);
    double IntegralSimpson(double a, double b, int N, int n);
    double int_func(double x, int n);
public:
    TalbotMath(double width, double period)
    {
        this->b = width;
        this->p = period;
    }

    double main_f(double x, int N);
};


#endif //TALBOT_TALBOTMATH_H
