#include <iostream>
#include <bits/stdc++.h>
using namespace std;

struct Data{
    int index;
    int val[2];
};

bool cmp1(Data a, Data b){
    return a.val[0]>b.val[0]; //descending order
}

bool cmp2(Data a, Data b){
    if(a.val[0]!=b.val[0]){
        return 0;
    }
    if((a.val[1]%2 == 1)&&(b.val[1]%2 == 0)){
        return 1;
    }
    if(a.val[1]%2 == b.val[1]%2){
        return a.val[1]<b.val[1]; //ascending order
    }
    return 0;
    
}

int main(){
    int n;
    cin >> n;
    Data data[n];
    for(int i=0;i<n;i++){
        for(int j=0;j<2;j++){
            cin >> data[i].val[j];
        }
    }
    for(int i=0;i<n;i++){
        data[i].index = i+1;
    }

    stable_sort(data,data+n,cmp1);
    stable_sort(data,data+n,cmp2);
    for(int i=0;i<n;i++){
        cout << data[i].index << " ";
    }
    return 0;
}