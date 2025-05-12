#include <iostream>
#include <bits/stdc++.h>
using namespace std;

int main(){
    int n,m;
    cin >> n >> m;
    map <string, int> dict;
    for(int i=0;i<n;i++){
        string str;
        int money;
        cin >> str >> money;
        dict[str] = money;
    }
    for(int i=0;i<m;i++){
        string str;
        int count = 0;
        while(cin >> str && str != "."){
            if(dict.count(str) != 0) count += dict[str];
        }
        cout << count << endl;
    }
}