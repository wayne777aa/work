#include <bits/stdc++.h>
using namespace std;

vector<string> v;
string word;
int num=0;

void Printword(){
    if(v.empty()) v.push_back(word);
    else{
        v.push_back(v.back());
        for(int i=v.size()-2;i>0;i--){
            v[i] = v[i-1];
        }
        v[0] = word;
    }
    cout << word;
    word = "";
}

void PrintNum(){
    string w = v[num-1];
    cout << w;
    for(int i=num-1;i>0;i--){
        v[i] = v[i-1];
    }
    v[0] = w;
    num = 0;
}

int main(){
    string s;
    word = "";
    while(getline(cin, s)){
        if(s == "0") break;
        s += '\n';
        for(int i=0;i<s.size();i++){
            if(isalpha(s[i])){
                word += s[i];
            }else if(isdigit(s[i])){
                num *= 10;
                num += s[i] - '0';   
            }else{
                if(num) PrintNum();
                if(word != "") Printword();
                cout << s[i];
            }
        }
    }
    return 0;
}