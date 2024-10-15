#include <stdio.h>
#include <time.h>
#define PROFILE 1
int getNumGoodOperators(int x, int y);

int main()
{
    int x, y;
    int num_good_operators;
    clock_t st, ed;

    scanf("%d %d", &x, &y);
    
    st = clock();
    num_good_operators = getNumGoodOperators(x, y);
    ed = clock();
    printf("%d\n", num_good_operators);
#ifdef PROFILE
    printf("Elapsed time: %.2lf sec\n", (double)(ed-st)/CLOCKS_PER_SEC);
#endif
  
    return 0;
}


int getNumGoodOperators(int x, int y)
{
    int good_cnt = 0;
    int num[2] = {0};
    
    for(int i = x+1; i<= x+y; i++){
        int temp = i;
        while(temp>0){
            num[temp%2]++;
            temp = temp/2;
        }
        if(num[0]>=num[1])
        good_cnt++;
        num[0] = 0;
        num[1] = 0;
    }
    

    return good_cnt;
}