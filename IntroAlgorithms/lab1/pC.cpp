#include <iostream>
#include <bits/stdc++.h>
using namespace std;

int main(){
    int N,K;
    cin >> N >> K;
    int H[N],X[K];
    for(int i=0;i<N;i++){
        cin >> H[i];
    }
    for(int i=0;i<K;i++){
        cin >> X[i];
    }
    int left = 0, right = *max_element(H,H+N);
    int ans = 0;
    while (left <= right) { //需有=號 否則會少跑一個最大值
        int mid = (left + right) / 2;
        int length=0,count=0;
        for(int i=0;i<N;i++){
            if(H[i]>=mid){
                length++;
                if(length==X[count]){
                    length = 0;
                    count++;
                    if(count==K){
                        left = mid+1;
                        ans = mid;
                        break;
                    }
                }
            }else{
                length = 0;
            }
        }
        if(count!=K) right = mid-1;
    }
    cout << ans;
    return 0;
}