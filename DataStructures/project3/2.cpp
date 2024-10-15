#include <iostream>
using namespace std;

int main(){
    string s;
    cin >> s;
    int revise=0;
    int leftcount=0;
    for(int i=0;i<s.length();i++){
        if(s[i] == '(')
            leftcount++;
        else{
            if(leftcount>0)
                leftcount--;
            else
                revise++;
        }
    }
    while(leftcount > 0){
        revise++;
        leftcount--;
    }
    cout << revise << endl;
    return 0;
}