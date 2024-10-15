#include <iostream>
#include <string.h>

using namespace std;
    
int main() {
    string s,st;
    while(cin>>s){
        char str[21];
        int len = s.length();
        if(len%2==0){
            for(int i=0;i<len;i++){
                str[i]=s[len-i-1];
            }
            str[21] = 0;
            st = str;
            if(s == st){
                cout<< s <<  "-- is a regular palindrome." << endl;
            }
        }else{
            
        }
    }
    cout<<s;
    return 0;
}