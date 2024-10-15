#include <iostream>
#include <bits/stdc++.h>
using namespace std;
const long long Mod = 998244353;

long long arr[1000000];
long long sorted[1000000];

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
    return cnt;
}

bool cmp(int a,int b){
    return a<b;
}

int main(){
    long long N,K;
    cin >> N >> K;
    long long input[2*N];
    for(int i=0;i<N;i++){
        cin >> input[i];
        input[i+N] = input[i];
    }
    long long cnt1=0;//循環一次出來的cnt
    long long cnt2=0;//循環完剩的數量去cnt
    long long over = (K%N)%Mod;
    copy(input, input+N, arr);
    long long num = merge_sort(arr,0,N-1)%Mod;
    copy(input, input+N, arr);
    sort(arr,arr+N,cmp);
    map<long long,long long> bigger,smaller;
    for(int i=0;i<N;i++){
        bigger[arr[i]]=N-1-i;
    }
    for(int i=N-1;i>=0;i--){
        smaller[arr[i]] = i;
    }
    if(K>=N){
        cnt1 = num%Mod;
        if(over>0)
        cnt2 = num%Mod;
        for(int i=0;i<N-1;i++){ //做到N-2(N-1排到第一位)
            num = (num + bigger[input[i]] - smaller[input[i]])% Mod; //(bigger) - (smaller)
                cnt1 = (cnt1 + num)%Mod;
            if(i<over-1){
                cnt2 = (cnt2 + num)%Mod;
            }
        }
    }else{
        if(over>0)
        cnt2 = num;
        for(int i=0;i<over-1;i++){ //做到N-2(N-1排到第一位)
            num = (num + bigger[input[i]] - smaller[input[i]])% Mod; //(N-rank-1) - (rank) +(repeat)
                cnt2 = (cnt2 + num)%Mod;
        }
    }
    long long route = K/N;
    route = route % Mod;
    cnt1 = (cnt1*route)%Mod;
    
//-------------不同循環間的數量-------------
    long long cnt3 =0;
    sort(input,input+N,cmp);
    sort(input+N,input+2*N,cmp);
    cnt3 = merge_sort(input,0,2*N-1)%Mod;
    long long temp = (K)%Mod;
    temp = ((temp*(temp-1))/2);
    temp %= Mod;
    cnt3 = (cnt3*temp)%Mod;
    long long result = ((cnt1+cnt2)%Mod+cnt3)%Mod;//1+2+3+...+K-1
    cout << result;
}