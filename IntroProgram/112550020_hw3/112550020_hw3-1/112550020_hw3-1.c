#include <stdio.h>
#include <limits.h>

int main()
{
    long long int num1, num2;
    __int128 result;
    char op;
    while(scanf("%lld %lld %c", &num1, &num2, &op) != EOF){
        if(op == '+')
        result = (__int128)num1 + num2;
        if(op == '-')
        result = (__int128)num1 - num2;
        if(LONG_MIN <= num1 && num1 <= ULONG_MAX && LONG_MIN <= num2 && num2 <= ULONG_MAX && LONG_MIN <= result && result <= ULONG_MAX){
            printf("Using the data type \"");
            if((CHAR_MIN <= num1 && num1 <= CHAR_MAX) && CHAR_MIN <= num2 && num2 <= CHAR_MAX && CHAR_MIN <= result && result <= CHAR_MAX){
            printf("char");
            }else if(0 <= num1 && num1 <= UCHAR_MAX && 0 <= num2 && num2 <= UCHAR_MAX && 0 <= result && result <= UCHAR_MAX){
            printf("unsigned char");
            }else if(SHRT_MIN <= num1 && num1 <= SHRT_MAX && SHRT_MIN <= num2 && num2 <= SHRT_MAX && SHRT_MIN <= result && result <= SHRT_MAX){
            printf("short int");
            }else if(0 <= num1 && num1 <= USHRT_MAX && 0 <= num2 && num2 <= USHRT_MAX && 0 <= result && result <= USHRT_MAX){
            printf("unsigned short int");
            }else if(INT_MIN <= num1 && num1 <= INT_MAX && INT_MIN <= num2 && num2 <= INT_MAX && INT_MIN <= result && result <= INT_MAX){
            printf("int");
            }else if(0 <= num1 && num1 <= UINT_MAX && 0 <= num2 && num2 <= UINT_MAX && 0 <= result && result <= UINT_MAX){
            printf("unsigned int");
            }else if(LONG_MIN <= num1 && num1 <= LONG_MAX && LONG_MIN <= num2 && num2 <= LONG_MAX && LONG_MIN <= result && result <= LONG_MAX){
            printf("long int");
            }else if(0 <= num1 && num1 <= ULONG_MAX && 0 <= num2 && num2 <= ULONG_MAX && 0 <= result && result <= ULONG_MAX)
            printf("unsigned long int");
            printf("\" can complete this arithmetic operation\n");
        }else
            printf("This arithmetic operation will overflow.\n");
    }
}

/*CHAR_MIN  : -128
CHAR_MAX  : 127
SHORT_MIN : -32768
SHORT_MAX : 32767
INT_MIN   : -2147483648
INT_MAX   : 2147483647
LONG_MIN  : -9223372036854775808
LONG_MAX  : 9223372036854775807*/