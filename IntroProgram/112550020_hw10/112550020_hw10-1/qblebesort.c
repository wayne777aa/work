#include <stdio.h>
#include <stdlib.h>
#include <time.h>
#define PROFILE profile
void swap(int *a, int *b){
    int temp = *a;
    *a = *b;
    *b = temp;
}

//Comparison function for qsort
int compare(const void* a, const void* b){
    //Cast void pointers to integers
    int num1 = *((int*)a);
    int num2 = *((int*)b);

    if (num1 > num2 * 2){
        printf("bub\n");
        return 1;
    } else if (num1 > num2){
        printf("ble\n");
        return 1;
    } else {
        printf("be\n");
        return -1;
    }

}

int main(){
    int *arr, n;
    int x, y;
    clock_t st, ed;
    st = clock();
    while(scanf("%d", &n) != EOF){
        st = clock();
        arr = malloc(n*sizeof(int));
        for(int i=0;i<n;i++){
            scanf("%d", &arr[i]);
        }
        qsort(arr, n, sizeof(int), compare);
        ed = clock();
#ifdef PROFILE
    printf("Elapsed time: %.2lf sec\n", (double)(ed-st)/CLOCKS_PER_SEC);
#endif
    }
}