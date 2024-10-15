# include <stdio.h>
# include <limits.h>

void read_input(long int arr[], int len){
    long int sum=0, min=arr[0], max=arr[0];
    double avg = 0;

    for(int i=0; i<len; i++){
        sum = sum + arr[i];
        if(arr[i]<min){
            min = arr[i];
        }
        if(arr[i]>max){
            max = arr[i];
        }
    }
    if(len != 0)
    avg = (double)sum/len;

    printf("number of integers: %d\n", len);
    printf("max: %ld\n", max);
    printf("min: %ld\n", min);
    printf("avg: %.2lf", avg);
}

int main(){

    long int arr[10000];
    int len = 0;
    for(int i=0; ;i++,len++){
        scanf("%ld", &arr[i]);
        if(arr[i] == 0)
        break;
    }

    read_input(arr, len);
    return 0;
}