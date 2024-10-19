#include <iostream>
#include <cstdlib>
#include <stack>
using namespace std;

struct vertex{
    int connect[26] = {-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1};
};

int main(){
    char c;
    cin >> c;
    int n = c - 'A'+1;
    stack<int> g;
    vertex ver[n];
    while(cin >> c){
        int v = c-'A';
        cin >> c;
        for(int i=0;i<26;i++){
            if(ver[v].connect[i] == -1){
                ver[v].connect[i] = (int)c - 'A';
                break;
            }
        }
        for(int i=0;i<26;i++){
            if(ver[(int)c-'A'].connect[i] == -1){
                ver[(int)c-'A'].connect[i] = v;
                break;
            }
        }
    }
    int visit[n]={0};
    int count = 0;
    for(int i=0;i<n;i++){
        if(visit[i] == 0){
            visit[i] = ++count;
        }else
            continue;
        g.push(i);
        while(!g.empty()){   
            int k = g.top();
            g.pop();
            visit[k] = count;
            for(int j=0;j<n;j++){
                if(ver[k].connect[j] != -1){
                    if(visit[ver[k].connect[j]] == 0)
                        g.push(ver[k].connect[j]);
                }else
                    break;
            }
        }
    }
    cout << count << endl;
    return 0;
}