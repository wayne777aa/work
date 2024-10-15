#include <stdio.h>
#include <stdlib.h>
#include <time.h>

int main(){
    srand(time(NULL));
    int n;
    int *arr, *count;

    printf("1\n1\n");

    for(int i=0; i<29; i++){
        n = rand()%10+11;
        while(n==1){
            n = rand()%20;
        }
        arr = malloc((n+1)*(sizeof(int)));
        count = calloc(n+1,(sizeof(int)));
        for(int j=0; j<n; j++){
            while(1){
                int a = rand()%n;
                if(count[a]!=1){
                    arr[j] = a;
                    count[arr[j]]++;
                    break;
                }
            }
        }
        printf("%d\n", n);
        printf("%d", arr[0]+1);
        for(int j=1; j<n; j++)
            printf(" %d", arr[j]+1);
        printf("\n");
        free(arr);
        free(count);
    }

    for(int i=0; i<69; i++){
        n = rand()%1000+1;
        arr = malloc((n+1)*(sizeof(int)));
        count = calloc(n+1,(sizeof(int)));
        for(int j=0; j<n; j++){
            while(1){
                int a = rand()%n;
                if(count[a]!=1){
                    arr[j] = a;
                    count[arr[j]]++;
                    break;
                }
            }
        }
        printf("%d\n", n);
        printf("%d", arr[0]+1);
        for(int j=1; j<n; j++)
            printf(" %d", arr[j]+1);
        printf("\n");
        free(arr);
        free(count);
    }

    arr = malloc(1000*(sizeof(int)));
    count = calloc(1000,(sizeof(int)));
    
    for(int j=0; j<1000; j++){
        while(1){
            int a = rand()%1000;
            if(count[a]!=1){
                arr[j] = a;
                count[arr[j]]++;
                break;
            }
        }
    }
    printf("1000\n");
    printf("%d", arr[0]+1);
        for(int j=1; j<1000; j++)
            printf(" %d", arr[j]+1);
    printf("\n");
}