#include <iostream>
#include <bits/stdc++.h>
using namespace std;

struct num{
    int i = -1;
    int count;
};

int main(){
    int n;
    cin >> n;
    num number[n];
    int kind=0;
    int c;
    for(int i=0;i<n;i++){
        cin >> c;
        for(int j=0;j<=kind;j++){
            if(number[j].i == c){
                number[j].count++;
                break;
            }
            if(j == kind){
                number[kind].i = c;
                number[kind].count = 1;
                kind++;
                break;
            }
        }
    }
    int ans=0;
    for(int i=0;i<kind;i++){
        if(number[i].count == 1){
            cout << -1 << endl;
            return 0;
        }
        while(number[i].count >= 5){
            number[i].count -=3;
            ans++;
        }
        switch (number[i].count){
            case 4:
                ans +=2;
                break;
            case 3:
                ans +=1;
                break;
            case 2:
                ans +=1;
                break;
        }
    }
    cout << ans << endl;
    return 0;
}