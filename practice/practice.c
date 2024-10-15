#include <stdio.h>

int main()
{
    int number, sum = 0, count = 0;
    float average;
    printf("Please enter the numbers (quit = 0):\n");
    do{
        scanf("%d", &number);
        sum += number;
        count++;
    } while (number != 0);
    count--;
    count != 0 && (average = (float)sum/count);
    if(count == 0){
        printf("the average is N/A\n");
    }else
        printf("the average is %.2f\n", average);
    
    return 0;
}