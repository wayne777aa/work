#include <iostream>
#include <bits/stdc++.h>
using namespace std;
const long long Mod = 998244353;

long long arr[1000000];
long long sorted[1000000];
map<long long,long long> bigger,smaller,turn;

long long merge_sort(long long *arr,long long l, long long r) {
    if (l >= r) return 0;
    long long mid = (l + r)/2;
    long long cnt = (merge_sort(arr,l, mid) + merge_sort(arr,mid + 1, r))% Mod;
    long long k = 0, i = l, j = mid + 1;
    while (i <= mid || j <= r){
        if(i <= mid && j <= r){
            if (arr[i] <= arr[j]){
                sorted[k++] = arr[i++];
            }else{
                sorted[k++] = arr[j++];
                cnt = (cnt + mid - i + 1)% Mod; //arr[i] > arr[j] 
            }
        }else{
            if(i <= mid) sorted[k++] = arr[i++];
            else sorted[k++] = arr[j++];
        }
    }
    for (int i = l, j = 0; i <= r; i++, j++) arr[i] = sorted[j];
    return cnt%Mod;
}

bool cmp(int a,int b){
    return a<b;
}

int main(){
    long long N,K;
    cin >> N >> K;
    long long input[1000000] = {0};
    for(int i=0;i<N;i++){
        cin >> input[i];
        input[i+N] = input[i];
    }
    long long cnt1=0;//循環一次的cnt
    long long cnt2=0;//循環完剩的數量去cnt
    long long over = (K%N)%Mod; //剩的數量
    copy(input, input+N, arr);
    long long num = merge_sort(arr,0,N-1);

    copy(input, input+N, arr);
    sort(arr,arr+N,cmp);    
    for(int i=0;i<N;i++){
        bigger[arr[i]]  = N-1-i;
    }
    for(int i=N-1;i>=0;i--){
        smaller[arr[i]] = i;
    }
    // cnt1 = num%Mod;
    // if(over>0)
    // cnt2 = num%Mod;
    // for(int i=0;i<N-1;i++){ //做到N-2(N-1排到第一位)
    //     num = (num + bigger[input[i]] - smaller[input[i]])% Mod; //(bigger) - (smaller)
    //         cnt1 = (cnt1 + num)%Mod;
    //     if(i<over-1){
    //         cnt2 = (cnt2 + num)%Mod;
    //     }
    // }
    // long long route = K/N;
    // route = route % Mod;
    // cnt1 = (cnt1*route)%Mod;
    // if(K<N){
    //     cnt1 = 0;
    // }
    
    copy(input, input+N, arr);
    for(int i=0;i<N;i++){
        turn[arr[i]]=bigger[arr[i]]-smaller[arr[i]];
    }
    long long ans=num,last=0;
    long long ans1=ans,ans2=ans;
    for(int i=0;i<over-1;i++){
        cnt2=(cnt2+ans2+turn[input[i]])%Mod;
        ans2=(ans2+turn[input[i]]);
    }
    for(int i=0;i<N;i++){
        cnt1=(ans1+cnt1+turn[input[i]])%Mod;
        ans1=(ans1+turn[input[i]]);
        if(i==N-1){
            last=ans1;
        }
    }
//-------------不同循環間的數量-------------
    long long cnt3 = 0;
    sort(input,input+N,cmp);
    sort(input+N,input+2*N,cmp);
    cnt3 = merge_sort(input,0,2*N-1);
    long long temp = K%Mod;
    temp = ((temp*(temp-1))/2)%Mod;
    cnt3 = (cnt3*temp)%Mod;

    ans=(ans+cnt2)%Mod;
    ans=(ans+((cnt1*((K/N)%Mod))%Mod))%Mod;
    ans=(ans+cnt3)%Mod;
    if(K%N==0){
    ans=(ans-last+Mod)%Mod;
    }
    cout << ans << endl;
}