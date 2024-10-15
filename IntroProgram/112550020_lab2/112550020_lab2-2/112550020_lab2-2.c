#include<stdio.h>

int main()
{
    int num1, num2;
    char op;
    scanf("%d %c %d", &num1, &op, &num2);

    switch (op)
    {
    case 43:    printf("%d", num1+num2);
                break;
    case 45:    printf("%d", num1-num2);
                break;
    case 42:    printf("%d", num1*num2);
                break;
    case 47:    if(num2 != 0){
                    printf("%.2f", (float)num1/num2);
                } else {
                    printf("divided by zero error");
                }
                break;
    default:
        break;
    }
    return 0;
}