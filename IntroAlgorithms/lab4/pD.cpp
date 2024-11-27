#include <bits/stdc++.h>
using namespace std;
#define IOS ios::sync_with_stdio(false);cin.tie(0);cout.tie(0);

long long d[5000][5000];
long long arr[5000];

long long findbest(int st, int ed, int person){ //0 represent faker, 1 represent Chovy
    if(st == ed){
        return (person == 0)? arr[st] : -arr[st];
    }
    if(d[st][ed] != -1) return d[st][ed];

    if(person == 0){
        d[st][ed] = max(arr[st] + findbest(st+1,ed,1), arr[ed] + findbest(st,ed-1,1));
    }else if(person == 1){
        d[st][ed] = min(findbest(st+1,ed,0) - arr[st], findbest(st,ed-1,0) - arr[ed]);
    }
    return d[st][ed];
}

int main(){
    IOS
    int n;
    cin >> n;
    for(int i=0;i<n;i++){
        cin >> arr[i];
        for(int j=0;j<n;j++){
            d[i][j] = -1;
        }
    }
    
    cout << findbest(0,n-1,0);
    return 0;
}

/*
4
7 10 2 6

7
10 14 9 15 17 16 5

6
10 14 9 15 17 16

*/