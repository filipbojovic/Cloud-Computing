#include<stdio.h>
#include<stdlib.h>
#include<time.h>
#include<math.h>

int main(int argc, char* argv[])
{

    int seed = atoi(argv[1]);
    unsigned long brojUzoraka = atoi(argv[2]);

    double pi = 0.0, x, y;

    srand(seed);
    double u;
    unsigned long  i, unutar = 0;

    for(i = 0; i < brojUzoraka; i++)
    {
        x = rand() * 1.0 / RAND_MAX;
        y = rand() * 1.0 / RAND_MAX;
        if ((x*x + y*y) <= 1.0)
            unutar += 1;
    }

    pi = 4.0 * (unutar  * 1.0 / brojUzoraka);

    // printf("%.10lf", pi);
    printf("%lu\n", unutar);
    
    return 0;
}