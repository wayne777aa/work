#include <iostream>
#include <bits/stdc++.h>
using namespace std;
const int Mod = 998244353;

long long arr[500000];
long long sorted[500000];

long long merge_sort(long long *arr,int l, int r) {
    if (l >= r) return 0;
    int mid = (l + r)/2;
    long long cnt = (merge_sort(arr,l, mid) + merge_sort(arr,mid + 1, r))% Mod;
    int k = 0, i = l, j = mid + 1;
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
    long long over = K%N;
    if(K>=N){
        copy(input, input+N, arr);
        long long num = merge_sort(arr,0,N-1);
        map<long long,long long> rank,repeat;
        long long ranknum = 0;
        for(int i=0;i<N;i++){
            if(arr[i] > arr[i-1]){
                rank[arr[i]] = ranknum;
            }
            if(arr[i] == arr[i-1]){
                rank[arr[i]] = ranknum;
                repeat[arr[i]]++;
            }
            ranknum++; //越大的排名越後面
        }
        cnt1 = num;
        if(over>0)
        cnt2 = num;
        for(int i=0;i<N-1;i++){ //做到N-2(N-1排到第一位)
            num = (num + (N - rank[input[i]] - 1) - (rank[input[i]]) + repeat[input[i]])% Mod; //(N-rank-1) - (rank)+(repeat)
                cnt1 = (cnt1 + num)%Mod;
            if(i<over-1){
                cnt2 = (cnt2 + num)%Mod;
            }
        }
    }else{
        copy(input, input+N, arr);
        long long num = merge_sort(arr,0,N-1);
        map<long long,long long> rank,repeat;
        long long ranknum = 0;
        for(int i=0;i<N;i++){
            if(arr[i] > arr[i-1])
                rank[arr[i]] = ranknum;
            if(arr[i] == arr[i-1]){
                rank[arr[i]] = ranknum;
                repeat[arr[i]]++;
            }
            ranknum++; //越大的排名越後面
        }
        if(over>0)
        cnt2 = num;
        for(int i=0;i<over-1;i++){ //做到N-2(N-1排到第一位)
            num = num + (N - rank[input[i]] - 1) - (rank[input[i]]) + repeat[input[i]]; //(N-rank-1) - (rank) +(repeat)
                cnt2 = (cnt2 + num)%Mod;
        }
    }
    int route = K/N;
    route = route % Mod;
    cnt1 = (unsigned long long)(cnt1*route)%Mod;
    
//-------------不同循環間的數量-------------
    unsigned long long cnt3;
    sort(input,input+N,cmp);
    sort(input+N,input+2*N,cmp);
    cnt3 = merge_sort(input,0,2*N-1);
    int temp = K%Mod;
    cnt3 = cnt3*(((temp*(temp-1))%Mod)/2);
    cnt3 = cnt3%Mod;
    long long result = ((cnt1+cnt2)%Mod+cnt3)%Mod;//1+2+3+...+K-1
    cout << result;
}