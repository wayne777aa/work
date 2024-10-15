#include <iostream>
#include <string.h>
using namespace std;

string reverse(int st, int en, string s){
    for(int a = 0; a < (en - st + 1) / 2; a++){
    swap(s[st + a],s[en - a]);
    }
    return s;
}

int main(){
    string s, s1, sp;
    int n, ksp = 1;
    cin >> n;
    cin >> s;
    sp = s;
    for(int k=1;k<n;k++){
        s1 = s;
        for(int i=0;i+k < n;i++){
            s1 = reverse(i, i+k, s1);
        }
        if(s1<sp){
            sp = s1;
            ksp = k+1;
        }
    }
    cout << sp << endl;
    cout << ksp << endl;
    return 0;
}