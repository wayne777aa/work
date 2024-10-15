#include <stdio.h>
#include <stdlib.h>
#include <time.h>
#define PROFILE profile
void swap(int *a, int *b){
    int temp = *a;
    *a = *b;
    *b = temp;
}

void bubblebe_sort (int *array,int n) {
    int i, j;
    for(i = 0; i<n; i++){ // from A to B, including B
        for(j = 0; j<n-i-1; j++){
            if (array[j] > array[j+1] * 2){
                printf("bub\n");
                swap(&array[j], &array[j+1]); // assuming this works
            }
            else if(array[j] > array[j+1]){
                printf("ble\n");
                swap(&array[j], &array[j+1]);
            }
            else{
                printf("be\n");
            }
        }
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
        bubblebe_sort(arr,n);
        ed = clock();
#ifdef PROFILE
    printf("Elapsed time: %.2lf sec\n", (double)(ed-st)/CLOCKS_PER_SEC);
#endif
    }
}