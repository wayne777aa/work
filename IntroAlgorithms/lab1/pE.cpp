#include <iostream>
#include <bits/stdc++.h>
using namespace std;

bool decmp(int a,int b){
    return a>b;
}

bool ascmp(int a,int b){
    return a<b;
}

int main(){
    int N,K;
    cin >> N >> K;
    long long int H[N],D[N];
    for(int i=0;i<N;i++){
        cin >> H[i];
    }
    for(int i=0;i<N;i++){
        cin >> D[i];
    }
    sort(H,H+N,ascmp);
    sort(D,D+N,decmp);
    long long left = 0, right = H[N-1]*D[0];
    long long int ans = 0;
    while (left <= right) {
        long long int mid = (left + right) / 2;
        long long int count=0;
        for(int i=0;i<N;i++){
            if((H[i]-(mid/D[i]))>0)
            count += H[i]-(mid/D[i]);
        }
        if(count<=K){
            ans = mid;
            right = mid-1;
        }else{
            left = mid+1;
        }
    }
    cout << ans;
    return 0;
}