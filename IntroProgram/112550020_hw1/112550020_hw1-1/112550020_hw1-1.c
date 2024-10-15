#include<stdio.h>

int main()
{
    int year,month,day;
    scanf("%d/%d/%d", &year, &month, &day);
    printf("Germany: %2.2d.%2.2d.%4.4d\n", day, month, year+1911);
    printf("Belgium: %2.2d/%2.2d/%4.4d\n", day, month, year+1911);
    printf("Taiwan: %4.4d/%2.2d/%2.2d\n", year+1911, month, day);
    printf("US: %2.2d/%2.2d/%2.2d\n", month, day, (year+1911)%100);
    printf("UK: %2.2d/%2.2d/%2.2d\n", day, month, (year+1911)%100);
    return 0;
}