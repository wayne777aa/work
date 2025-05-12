#include <iostream>
#include <bits/stdc++.h>
using namespace std;
int maxn = 10005;
bool NP[10005] = {0};
vector<int> v;


int main(){
    for(int i=2; i<maxn; i++){
        if(NP[i] == 0){
            for(int j=i+i;j<maxn;j+=i){
                NP[j] = true;
            }
            v.push_back(i);
        }
    }
    int n;
    while(cin >> n){
        if(n==0) break;
        int count=0;
        for(int i=0;v[i]<= n;i++){
            int sum=0;
            for(int j=i;sum<n;j++){
                sum += v[j];
                if(sum == n){
                    count++;
                }
            }
        }
        cout << count << endl;
    }
    return 0;
}