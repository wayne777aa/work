#include <stdio.h>

long long power(int base, int exp) {
    if (exp == 0) {
        return 1;
    }
    return power(base, exp - 1) * base;
}

int main() {
    // DO NOT modify this section
    int n, d;
    printf("Enter base (positive integers): ");
    scanf("%d", &n);
    printf("Enter exponent (positive integers): ");
    scanf("%d", &d);

    printf("%lld\n", power(n, d));

    return 0;
}
