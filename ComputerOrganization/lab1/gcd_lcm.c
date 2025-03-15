#include <stdio.h>

int gcd(int a, int b) {
    int i=a;
    if(a>b){
        i=b;
    }
    while(i>0){
        if(a%i == 0 && b%i == 0)    return i;
        i--;
    }
    return 1;
}

int lcm(int a, int b) {
    int temp = gcd(a,b);
    return (a*b)/temp;
}

int main() {
    // DO NOT modify this section
    int n1, n2;
    printf("Please enter the first number: ");
    scanf("%d", &n1);
    printf("Please enter the second number: ");
    scanf("%d", &n2);

    printf("%d %d\n", gcd(n1, n2), lcm(n1, n2));

    return 0;
}
