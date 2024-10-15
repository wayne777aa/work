#include <iostream>
#include <bits/stdc++.h>
using namespace std;

struct num{
    int i = -1;
    int count;
};

int main(){
    num number[100000];
    int kind=0;
    int c;
    while(cin >> c){
        for(int j=0;j<=kind;j++){
            if(number[j].i == c){
                cout << "true" << endl;
                return 0;
            }
            if(j == kind){
                number[kind].i = c;
                number[kind].count = 1;
                kind++;
                break;
            }
        }
    }
    cout << "false" << endl;
    return 0;
}