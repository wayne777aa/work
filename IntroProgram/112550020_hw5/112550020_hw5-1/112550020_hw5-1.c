#include <stdio.h>

void swap(int *a, int *b){
    int tmp = *a;
    *a = *b;
    *b = tmp;
}

void reverseMat(int *arr,int m,int n){
    int i, j;
    for(i=0 ; i<m ;i++){
        for(j=0; j<n && i*n+j < (m*n)/2; j++){ //i*n+j < (m*n)/2避免重複交換
            swap(arr+i*n+j,arr+(m-1-i)*n+n-j-1); //交換 其實我覺得我直接寫一維比較實在
        }
    }
}


int main(){
    int m, n;
    scanf("%d %d", &m , &n);
    int arr[m][n];
    for(int i=0 ; i<m ; i++){
        for(int j=0 ; j<n ; j++){
            scanf("%d", &arr[i][j]);
        }
    }
    
    reverseMat((int *)arr,m,n); //傳送了arr中的(0,0)的位址 和幾列幾行

    for(int i=0 ; i<m ; i++){
        for(int j=0 ; j<n ; j++){
            printf("%d ", arr[i][j]);
        }
        printf("\n");
    }

    return 0;
}

