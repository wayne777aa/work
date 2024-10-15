#include <stdio.h>

int main(){
    int N, i,j;
    scanf("%d",&N);
    int arr[N], copy[N];
    for(i=0; i<N; i++)
        scanf("%d", &arr[i]);

    for(i=0; i<N; i++){ //由小排到大
        for(j=i+1; j<N; j++){
            if(arr[i]>arr[j]){
                int temp = arr[i];
                arr[i] = arr[j];
                arr[j] = temp;
            }
        }
    }

    for(i=0; i<N; i++){
        copy[i] = arr[i];
    }

    for(i=0,j=1; i<N/2; i++,j++){ //負的
        arr[i+j] = copy[i];
    }

    for(i=N/2,j = N/2; i<N; i++,j--) //正的
        arr[i-j] = copy[i];

    for(i=0; i<N; i++)
        printf("%d ",arr[i]);
}