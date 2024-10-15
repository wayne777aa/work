#include <stdio.h>

void reverse(int n, int *ans){
    while(n>0){
        *ans *= 10;
        *ans += n%10;
        n /= 10;
    }
    while(n<0){
        *ans *= 10;
        *ans += n%10;
        n /= 10;
    }
}

int main(){
    int n, ans=0;
    scanf("%d", &n);
    reverse(n, &ans);
    printf("%d", ans);
    return 0;
}