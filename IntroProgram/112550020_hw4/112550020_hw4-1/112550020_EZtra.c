#include <stdio.h>

int main(){
    int N, M, E, sum, ans = -2147483648, x, y;
    scanf("%d %d", &N , &M);
    int a[N][M];
    for(int i=0; i<N; i++){
        for(int j=0; j<M; j++){
            scanf("%d", &a[i][j]);
        }
    }
    scanf("%d", &E);
    for(int i=0; i<N; i++){
        for(int j=0; j<M; j++){
            sum = 0;
            sum += a[i][j];
            for(int k = 1; i-k >= 0 && k <= E;k++ ){
                if(a[i-k][j] == -100001)
                break;
                sum += a[i-k][j];
            }
            for(int k = 1; i+k <= N-1 && k <= E;k++ ){
                if(a[i+k][j] == -100001)
                break;
                sum += a[i+k][j];
            }
            
            for(int k = 1; j-k >= 0 && k <= E;k++ ){
                if(a[i][j-k] == -100001)
                break;
                sum += a[i][j-k];
            }
            for(int k = 1; j+k <= M-1 && k <= E;k++ ){
                if(a[i][j+k] == -100001)
                break;
                sum += a[i][j+k];
            }
            if(sum >= ans){
            ans = sum;
            x = i; y = j;
            }
        }
    }
    printf("(%d,%d) %d", x, y, ans);
    return 0;
}