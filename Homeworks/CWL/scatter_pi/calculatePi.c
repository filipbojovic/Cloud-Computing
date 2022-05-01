#include <stdio.h>
#include <stdlib.h>

int main(int argc, char **argv)
{
    int brojUzoraka = atoi(argv[1]) * (argc - 2);

    int ukupanBrojPogodaka = 0;
    for (int i = 2; i < argc; i++)
    {
        ukupanBrojPogodaka += atoi(argv[i]);
    }

    double pi = 4.0 * ukupanBrojPogodaka / brojUzoraka;

    printf("PI = %lf", pi);
}