#include <iostream>
#include <bits/stdc++.h>
using namespace std;

int A[1000000];

int main(){
    int N;
    cin >> N;
    for(int i=0;i<N;i++){
        cin >> A[i];
    }
    pair<int,int> min_index;
    int min=INT_MAX;
    for(int i=0;i<N;i++){
        long long V=A[i];
        for(int j=i+1;j<N;j++){
            long long D=j-i+1;
            V += A[j];
            if(V > 100000000) continue;
            if(V*V+D*D < min){
                min_index.first = i;
                min_index.second = j;
                min = V*V+D*D;
            }
        }
    }
    cout << min_index.first+1 << " " << min_index.second+1;
}