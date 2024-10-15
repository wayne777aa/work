#include <iostream>
#include <stack>
using namespace std;

string repeat(int num,string temp){
    string s;
    for(int i=0;i<num;i++){
        s += temp;
    }
    return s;
}

int main(){
    string s;
    cin >> s;
    stack<int> nums;
    int num=0;
    stack<string> s1;
    string temp;
    
    for(char c:s){
        if(isalpha(c)){
            temp += c;
        }else if(isdigit(c)){
            num = num*10 + ((int)c - '0');
        }else if(c == '['){
            s1.push(temp);
            temp = "";
            nums.push(num);
            num = 0;
        }else if(c == ']'){
            int times = nums.top();
            nums.pop();
            string pre_s = s1.top();
            s1.pop();
            pre_s += repeat(times,temp);
            temp = pre_s;
        }
        
    }
    cout << temp << endl;
    return 0;
}