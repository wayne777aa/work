#include <iostream> 
using namespace std; 
 
string repeat(int num,string temp){ 
    string s; 
    for(int i=0;i<num;i++){ 
        s += temp; 
    } 
    return s; 
} 
 
int readnum(string s){ 
    for(int i=0;i<s.size();i++){ 
        if(isdigit(s[i])) 
            return 1; 
    } 
    return 0; 
} 
 
int main(){ 
    string s,s1; 
    cin >> s; 
 
    while(readnum(s)){ 
        int i=0; 
        s1.clear(); 
        for(;i<s.size();){ 
            int num=0; 
            while(s[i]!='[' && s[i]!= 0 ){ 
                if(isalpha(s[i])){ 
                    s1 += s[i]; 
                    i++; 
                    continue; 
                } 
                if(isdigit(s[i])){ 
                    num = num*10 + (int)s[i] - 48; 
                    i++; 
                } 
            } 
            if(s[i] == 0)
                break;
            int left=1; 
            string temp; 
            i++; 
            while(left){ 
                if(s[i] == '['){ 
                    left++; 
                    temp += "["; 
                }else if(s[i] == ']'){ 
                    if(left > 1){ 
                        temp += "]"; 
                    } 
                    left--; 
                     
                }else{ 
                    temp += s[i]; 
                } 
                i++; 
            } 
            s1 += repeat(num,temp); 
        } 
        s = s1; 
    } 
    cout << s << endl; 
    return 0; 
}  