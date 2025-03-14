#include <stdio.h>

void findMaxMin(int arr[], int size, int* max, int* min) {
    //TODO
    *max = arr[0],*min = arr[0];
    for(int i=1;i<size;i++){
        if(*max<arr[i]) *max = arr[i];
        if(*min>arr[i]) *min = arr[i];
    }
    return;
}

int main() {
    // DO NOT modify this section
    int numbers[5];
    printf("Enter five positive integers: ");
    for (int i = 0; i < 5; i++) {
        scanf("%d", &numbers[i]);
    }

    int max, min;
    findMaxMin(numbers, 5, &max, &min);

    printf("%d %d\n", max, min);

    return 0;
}
