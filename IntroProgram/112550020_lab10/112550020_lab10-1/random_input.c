#include <stdio.h>
#include <stdlib.h>
#include <time.h>

int main(){
    srand(time(NULL));
    int n;
    int *arr, *count;
    
        scanf("%d", &n);
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

    printf("\n");
}