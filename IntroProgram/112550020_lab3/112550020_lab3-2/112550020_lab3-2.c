#include<stdio.h>

int main()
{
    int N, i, sum, N2;
    while(scanf("%d", &N) != EOF){
        i = 1; sum = 0; N2 = 0;
        while(i<N){
            if(N%i == 0){
                sum += i;
            }
            i++;
        }
        i = 1;
        while(i<sum){
            if(sum%i == 0){
                N2 += i;
            }
            i++;
        }
        if(sum == N)
        printf("%d is a perfect number.\n",N);
        else if(N == N2)
        printf("%d's amicable number is %d.\n", N, sum);
        else
        printf("%d is not a perfect number and does not have amicable number.\n", N);

    }
    return 0;
}