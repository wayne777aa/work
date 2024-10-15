#include<stdio.h>

int main()
{
    int a, b;
    float A, B;
    scanf("%d %d", &a, &b);
    A = a;
    B = b;
    printf("num1=%d, num2=%d in decimal\n", a, b);
    printf("num1=%o, num2=%o in octal\n", a, b);
    printf("num1=%x, num2=%x in hexadecimal\n", a, b);
    printf("(%d)+(%d)=%d\n", a, b, a+b);
    printf("(%d)-(%d)=%d\n", a, b, a-b);
    printf("(%d)*(%d)=%d\n", a, b, a*b);
    printf("(%d)/(%d)=%d\n", a, b, a/b);
    printf("(%d)%(%d)=%d\n", a, b, a%b);
    printf("(%d)/(%d)=%.2f\n", a, b, A/B);
    printf("(%d)/(%d)=%.2e in scientific notation\n", a, b, A/B);
    
    return 0;
}