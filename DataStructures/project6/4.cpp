#include <iostream>
#include <bits/stdc++.h>
using namespace std;


int main(){
    int n;
    cin >> n;
    int arr[n];
    for(int i=0;i<n;i++){
        cin >> arr[i];
    }

    int ans=0;
    for(int i=0;i<n;i++){
        for(int j=i+1;j<n;j++){
            if((arr[j]+i) == (arr[i]+j)){
                ans++;
            }
        }
    }
    cout << ans << endl;
    return 0;
}