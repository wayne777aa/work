#include<stdio.h>

int main()
{
    int bananas, monkeys;
    scanf("%d %d",&bananas, &monkeys);

    if(monkeys*8 == bananas){
        printf("%d",monkeys);
    } else
    if(monkeys*8 < bananas){
        if(bananas == (monkeys-1)*8+4)
        printf("%d",monkeys-2);
        else
        printf("%d",monkeys-1);
    } else 
    if(monkeys*8 > bananas){
        if(bananas == (monkeys-1)*8+4) 
        printf("%d",monkeys-2);
        else if(monkeys > bananas) //有猴子沒拿到香蕉
        printf("monkeys QQ");
        else
        printf("%d",((bananas-monkeys)/7)); //先全部分一根
    } else
    printf("monkeys QQ");
    return 0;
}