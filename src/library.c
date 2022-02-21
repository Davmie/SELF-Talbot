#include "library.h"

#include <stdio.h>
#include <math.h>
#include <stdlib.h>
#include <gsl/gsl_integration.h>
#include <gsl/gsl_errno.h>

#define TWO_PI 2 * M_PI
#define WAVE_LENGTH 5 * pow(10, -7)

static double F(double x)
{
    if (x < 0)
        return 0;
    if (x == 0)
        return 1.0 / 2;
    return 1;
}

static double f0(TalbotMath *st, double x)
{
    double coef = (TWO_PI) * x / st->p;

    if (!st->mode)
        return 1.0 / 2 * (1 + cos(coef));
    else
        return F(cos(coef) - cos(M_PI * (st->b / st->p)));
}

double integ_real_func(double x, void *p)
{
    TalbotMath *st = (TalbotMath *) p;

    double complex arg = x * st->omega_n * (-I);

    return creal(f0(st, x) * cexp(arg));
}

double integ_imag_func(double x, void *p)
{
    TalbotMath *st = (TalbotMath *) p;

    double complex arg = x * st->omega_n * (-I);

    return cimag(f0(st, x) * cexp(arg));
}

static double complex fn(TalbotMath *st)
{
    gsl_set_error_handler_off();
    gsl_integration_workspace *w = gsl_integration_workspace_alloc(1000);

    gsl_function F_real;
    F_real.function = &integ_real_func;
    F_real.params = st;

    gsl_function F_imag;
    F_imag.function = &integ_imag_func;
    F_imag.params = st;

    double result_real, error;
    gsl_integration_qags(&F_real, -st->p / 2, st->p / 2, 0, 1e-10,
                        1000, w, &result_real, &error);

//    double result_imag;
//    gsl_integration_qags(&F_imag, -st->p / 2, st->p / 2, 0, 1e-10,
//                        1000, w, &result_imag, &error);

    double complex res = result_real + 0 * I;

    gsl_integration_workspace_free(w);

    return 1.0 / st->p * res;
}

static void count_integrals(TalbotMath *st)
{
    for (int i = -st->n; i < st->n + 1; ++i)
    {
        st->omega_n = st->omega * (double) i;
        st->integrals[i + st->n] = fn(st);
    }
}

static double complex f(TalbotMath *st, double x, double z)
{
    double complex sum = 0;
    for (int i = -st->n; i < st->n + 1; ++i)
    {
        st->omega_n = (double) i * st->omega;
        sum += st->integrals[i + st->n] * cexp(I * (st->omega_n * x +
                csqrt(st->k * st->k - st->omega_n * st->omega_n) * z));
    }

    return sum;
}

double Intense(TalbotMath *st, double x, double z)
{
    return pow(cabs(f(st, x, z)), 2);
}

TalbotMath *create(double p, int mode, int n, double b)
{
    TalbotMath *st = malloc(sizeof(TalbotMath));
    if (st)
    {
        st->p = p;
        st->mode = mode;
        st->n = n;
        st->b = b;
        st->l = WAVE_LENGTH;
        st->omega = (TWO_PI) / st->p;
        st->k = (TWO_PI) / st->l;
        st->omega_n = -st->n * st->omega;

        st->integrals = malloc(sizeof(double complex) * (st->n * 2 + 1));
        if (!st->integrals)
            return NULL;

        count_integrals(st);
    }

    return st;
}

void free_TalbotMath(TalbotMath *st)
{
    if (st)
        free(st->integrals);
    free(st);
}
