#include<stdio.h>

int main()
{
    int x;
    while(scanf("%d", &x) != EOF){
        for(int i = 1 ; i <= 3+2*x; i++){
            if(i==1){                       //1st
                printf("*");
                for(int j = 0; j < 3+2*(x-1); j++)
                printf(" ");
                printf("* *");
                for(int j = 0; j < 3+2*(x-1); j++)
                printf(" ");
                printf("*  ");
                for(int j = 0; j < 3+2*(x-1); j++)
                printf("*");
                printf("  *");
                for(int j = 0; j < 3+2*(x-1); j++)
                printf(" ");
                printf("*\n");
            }
            if(i != 1 && i != 3+2*x){       //mid
                //N
                printf("*");
                for(int j = 0; j < i-2; j++)
                printf(" ");
                printf("*");
                for(int j = 0; j < 2*x-i+2 ; j++)
                printf(" ");
                printf("*");
                //Y
                if(i<=x+1){
                    for(int j = 0; j < i; j++)
                    printf(" ");
                    printf("*");
                    for(int j = 0; j < 2*x-1-2*(i-2); j++)
                    printf(" ");
                    printf("*");
                    for(int j = 0; j < i ; j++)
                    printf(" ");
                } else {
                    for(int j = 0; j < x+2 ; j++)
                    printf(" ");
                    printf("*");
                    for(int j = 0; j < x+2 ; j++)
                    printf(" ");
                }
                //C
                if(i == 2 || i == 3+2*x-1){
                    printf("*");
                    for(int j = 0; j < 3+2*(x-1); j++)
                    printf(" ");
                    printf("* ");
                } else {
                    printf("*");
                    for(int j = 0; j < 3+2*(x-1)+2; j++)
                    printf(" ");
                }
                //U
                printf("*");
                for(int j = 0; j < 3+2*(x-1); j++)
                printf(" ");
                printf("*");

                printf("\n");
                
            }
            if(i==3+2*x){                   //last
                printf("*");
                for(int j = 0; j < 3+2*(x-1); j++)
                printf(" ");
                printf("* ");
                for(int j = 0; j < x+1; j++)
                printf(" ");
                printf("*");
                for(int j = 0; j < x+3; j++)
                printf(" ");
                for(int j = 0; j < 3+2*(x-1); j++)
                printf("*");
                for(int j = 0; j < 3 ;j++)
                printf(" ");
                for(int j = 0; j < 3+2*(x-1); j++)
                printf("*");
                printf(" \n");
            }
        }
    }
}