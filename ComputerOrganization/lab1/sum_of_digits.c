#include <stdio.h>

int sumOfDigits(int n) {
    // TODO
    int sum=0;
    while(n>0){
        sum += n%10;
        n /= 10;
    }
    return sum;
}

int main() {
    // DO NOT modify this section
    int num;
    printf("Enter an integer: ");
    scanf("%d", &num);

    printf("%d\n", sumOfDigits(num));

    return 0;
}
