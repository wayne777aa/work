#include <stdio.h>

int main(){
    int one_digit_num = 0, count[10]={0}; //1000000000000改成10
    char input_number;
    while(scanf("%c", &input_number) != EOF){ //要!= EOF 否則會無限循環出不了迴圈
        if(input_number != '-'){
            count[input_number - '0']++;
        }
    }
    for(int i = 0; i <= 9; i++)
        if(count[i] == 1)    //要=改==
            one_digit_num++;
    if(!one_digit_num)
        printf("\\/\\'_'/|/");  //少兩個\會輸出成/'_'/|/ 改\\/\\'_'/|/
    else{
        if(one_digit_num == 1)
            printf("Once occurrence digit: ");
        else
            printf("Once occurrence digits: "); //要輸出digits因為不只一個數
        for(int i = 0; i <= 9; i++)  //輸出會少跑"9" i < 9要改成 i <= 9
            if(count[i] == 1)
                printf("%d ", i); //少了一個' '(space)
    }
    return 0;
}