#include <iostream>
// #include <string.h>
using namespace std;


int main() {
    string s,st,ts; //st把s倒轉，ts把st轉換過
    while(cin>>s){
        char str[21] = {0};
        int len = s.length();
        for(int i=0;i<len;i++){
                str[i]=s[len-i-1];
            }
            st = str;
            ts = st;
            for(int i=0;i<len;i++){
                if(ts[i] == 'E'){
                    ts[i] = '3';
                    continue;
                }
                if(ts[i] == 'J'){
                    ts[i] = 'L';
                    continue;
                }
                if(ts[i] == 'L'){
                    ts[i] = 'J';
                    continue;
                }
                if(ts[i] == 'S'){
                    ts[i] = '2';
                    continue;
                }
                if(ts[i] == 'Z'){
                    ts[i] = '5';
                    continue;
                }
                if(ts[i] == '2'){
                    ts[i] = 'S';
                    continue;
                }
                if(ts[i] == '3'){
                    ts[i] = 'E';
                    continue;
                }
                if(ts[i] == '5'){
                    ts[i] = 'Z';
                    continue;
                }
            }
            if(s == ts && st == ts){
                cout<< s <<  " -- is a mirrored palindrome." << endl;
                continue;
            }
            if(s == ts){
                cout<< s <<  " -- is a mirrored string." << endl;
                continue;
            }
            if(s == st){
                cout<< s <<  " -- is a regular palindrome." << endl;
                continue;
            }
            cout << s << " -- is not a palindrome." << endl;
    
    }
    return 0;
}