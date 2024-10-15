#include <iostream>
#include <bits/stdc++.h>
using namespace std;

bool cmp(int a,int b){
    return a>b;
}

int main(){
    int N,K;
    cin >> N >> K;
    int arr[N];
    for(int i=0;i<N;i++){
        cin >> arr[i];
    }
    
    
    //--------循環一次的數量-----
    int cnt1=0;
    int route = K/N;
    for(int i=0;i<N;i++){
        for(int j=i+1;j<N;j++){
            if(arr[i]>arr[j])
                cnt1 = cnt1+i+1;
        }
        for(int j=i-1;j>=0;j--){
            if(arr[i]>arr[j])
                cnt1 = cnt1 + i-j;
        }   
    }
    cnt1 = cnt1*route;

    //--------循環完剩的數量--------------
    int cnt2=0;
    int over = K%N;
    int a[N*over] ={0};
    for(int i=0;i<over;i++){
        for(int j=0;j<N;j++){
            a[i*N+j] = arr[(j+i)%N];
        }
    }
    for(int i=0;i<over;i++){
        for(int j=i*N;j<(i+1)*N;j++){
            for(int k=j+1;k<(i+1)*N;k++)
            if(a[j]>a[k]){
                cnt2++;
            }
        }
    }
    
    //---------不同序列之間的逆序列數量---------
    sort(arr,arr+N,cmp);
    int cnt3=0;
    for(int i=0;i<N;i++){
        for(int j=i+1;j<N;j++){
            if(arr[i]>arr[j]){
                cnt3 += (N-1)-j+1;
                break;
            }
        }
    }
    long long result = (cnt1)+(cnt2)+(cnt3*(K*(K-1)/2));//1+2+3+...+K-1
    cout << result;
}