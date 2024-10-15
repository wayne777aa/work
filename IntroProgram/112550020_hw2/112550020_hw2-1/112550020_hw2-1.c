#include<stdio.h>

int main()
{
    char ch;
    scanf("%c",&ch);
    if(ch>=48 && ch<=57)
    printf("digit"); else
    if(ch>=65 && ch<=90)
    printf("uppercase letter"); else
    if(ch>=97 && ch<=122)
    printf("lowercase letter");
    else
    printf("other");
    return 0;
}