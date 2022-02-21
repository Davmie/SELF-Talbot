#ifndef UNTITLED4_LIBRARY_H
#define UNTITLED4_LIBRARY_H

#include <complex.h>

typedef struct
{
    double p;
    int mode;
    int n;
    double b;
    double l;
    double omega;
    double k;
    double omega_n;

    double complex *integrals;
}
TalbotMath;

double Intense(TalbotMath *st, double x, double z);
TalbotMath *create(double p, int mode, int n, double b);
void free_TalbotMath(TalbotMath *st);

#endif //UNTITLED4_LIBRARY_H
