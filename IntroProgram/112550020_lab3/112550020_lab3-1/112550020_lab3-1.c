#include<stdio.h>

int main()
{
    int Price, Pocket_money, Refund, Number, unuse, cap , use , bonus;
    while(scanf("%d %d %d %d", &Price, &Pocket_money, &Refund, &Number) != EOF){ //使用ctrl+d停止程式
        use = 0; unuse = 0;
        while(Pocket_money >= Price){
            unuse = unuse + (Pocket_money / Price);
            cap = Pocket_money/Price;
            while(unuse >= Number){ 
                bonus = (unuse/Number);
                unuse = unuse - bonus*Number;
                unuse += bonus;
                use += bonus * Number;
                cap += bonus;
            }
            
            Pocket_money = cap * Refund + Pocket_money % Price;
            cap = 0;
        }
        printf("%d\n", use + unuse);
    }
}