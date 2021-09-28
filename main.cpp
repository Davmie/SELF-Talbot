#include <iostream>

#include "TalbotMath.h"

#define WIDTH 5
#define PERIOD 10
#define ITERATIONS 100

int main()
{
    TalbotMath talbot(WIDTH, PERIOD);

    for (int j = 1; j < ITERATIONS; j++)
        std::cout << talbot.main_f(1, j) << '\n';
}