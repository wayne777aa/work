#include <iostream>
#include <string>
#include <climits>
using namespace std;


int main(){
    int n;
    cin >> n;
    string s;
    getline(cin,s);
    for(int i=0;i<n;i++){
        getline(cin,s);
        int W[13];
        int sum=0,j=0;
        if(i<n-1){
            int w=0;
            for(int j=0;j<s.size()-1;j++){ //除了最後一次以外 都要-1,oj才會對 但是自己的輸出不對
                if(s[j]==' ' || s[j] == '\0'){
                    W[sum++]=w;
                    w=0;
                }else{
                    if(s[j]!='0'){
                        w*=32;
                        w+=(int)s[j]-96;
                    }
                }
            }
            W[sum++] = w;
        }else{
            for(;sum<13;){     //initialize w
                int w=0;
                while(s[j]!=' '){
                    if(s[j] == 0) break;
                    w *= 32;
                    w += s[j++] - 'a' +1;
                }
                W[sum++] = w;
                if(s[j] == 0)   break;
                j++;
            }
        }

    
        int C=1;
        while(1){
            int flag =0;
            for(int k=0;k<sum;k++){
                int hash = (C/W[k])%sum;
                for(int q=k+1;q<sum;q++){
                    if((C/W[q])%sum == hash){
                        C = min((C/W[k]+1)*W[k],(C/W[q]+1)*W[q]);
                        flag =1;
                        break;
                    }
                }
                if(flag == 1) break;
            }
            if(flag == 0) break;
        }
        int min=INT_MAX;
        for(int k=0;k<sum;k++){
            if(C%W[k] == 0){
                min = 1;
                break;
            }
            if(W[k]<min)
                min = W[k];
        }
        C *= min;
        cout << s << endl;
        cout << C << '\n' << endl;
    }
    return 0;
}