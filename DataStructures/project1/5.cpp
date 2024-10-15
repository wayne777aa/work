#include <iostream>
#include <unordered_set>
using namespace std;

int main(){
    int n, count=0;
    cin >> n;
    unordered_set<string> s;
    string str[n];
    string str1,str2;
    for(int i=0;i<n;i++){
        cin >> str[i];
        s.insert(str[i]);
    }
    for(int i=0;i<n-1;i++){
        for(int j=i+1;j<n;j++){
            str1 = str[i];
            str2 = str[j];
            char a = str1[0];
            str1[0] = str2[0];
            str2[0] = a;
            if(s.count(str1))
                continue;
            if(s.count(str2))
                continue;
            count++;
        }
    }
    cout << count*2 <<endl;
    return 0;
}