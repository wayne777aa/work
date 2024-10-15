#include<stdio.h>

int main()
{
    int loan1,loan2;
    float rate, period;   //loan amount, annual interest rate, loan period
    scanf("$%d,%d %f %f", &loan1, &loan2, &rate, &period);
    int loan = loan1*1000+loan2;
    printf("| $2000| $1000| $500| $100| $10| $1|\n");
    printf("|%6d|%6d|%5d|%5d|%4d|%3d|\n", loan/2000, (loan%2000)/1000, (loan%1000)/500, (loan%500)/100, (loan%100)/10, (loan%10));
    printf("Monthly interest rate: %.2f%%\n", rate/12);
    printf("Total loan amount: %.1f\n", (float)loan*(1+(float)rate/12/100*(float)period));
    return 0;
}