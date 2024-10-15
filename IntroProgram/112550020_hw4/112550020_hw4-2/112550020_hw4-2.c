#include<stdio.h>

int a[1024];

int Duel(int left,int right){
    if((left +1)!= right){
        int mid = (left+right)/2;
        left = Duel(left, mid);
        right = Duel(mid +1, right);
        if(a[left] >= a[right]){
            a[left] = a[left] - a[right];
            return left;
        }else{
            a[right] = a[right] - a[left];
            return right;
        }
    }else if(a[left] >= a[right]){
        a[left] = a[left] - a[right];
        return left;
    }else{
        a[right] = a[right] - a[left];
        return right;
    }
}

int main()
{
    int N, winner;
    scanf("%d", &N);
    for(int i = 0; i<N ; i++)
        scanf("%d", &a[i]);
    if(N != 1){
    winner = Duel(0, N-1);
    }else winner = 0;
    printf("%d %d", winner, a[winner]);
}