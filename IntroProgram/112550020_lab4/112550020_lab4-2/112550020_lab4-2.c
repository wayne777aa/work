#include <stdio.h>

int a[100];

int binarySearch(int target, int head, int tail){
    int mid = (head + tail) / 2;
    if(a[mid] == target)
        return mid;
    else if(a[mid] > target){
        return binarySearch(target, head, tail = mid -1);
    }
    else{
        return binarySearch(target, head = mid + 1, tail);
    }
}


int main(){
    int N, target, i, j;
    scanf("%d", &N);

    for(i=0;i<N;i++)
    scanf("%d", &a[i]);

    scanf("%d", &target);

    int head = 0 , tail = N-1;
    int position = binarySearch(target, head, tail);
    printf("%d", position);
    return 0;

}