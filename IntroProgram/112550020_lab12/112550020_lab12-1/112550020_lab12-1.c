# include <stdio.h>
# include <stdlib.h>

int main(){
    unsigned long long int i = 0;
    int n, count = 0;
    while(scanf("%d", &n) != EOF){
        i |= ((unsigned long long int)1<<(n-1)); //會overflow 因為整數預設是int
    }

    for(int j = 0;j<64; j++){
        if (i & (unsigned long long int)1 << j){
            printf("%d ", j+1);
        }
    }
    return 0;
}