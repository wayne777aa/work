#include <bits/stdc++.h>
using namespace std;
#define IOS ios::sync_with_stdio(false);cin.tie(0);cout.tie(0);

struct cake{
    int index;
    int D;
    int P;
    double ratio;
}c[1000000];

bool cmp(cake a,cake b){
    if(a.ratio!=b.ratio) return a.ratio>b.ratio;
    else return a.index < b.index;
}

int main(){
    IOS
    int T;
    cin >> T;
    for(int i=0;i<T;i++){
        int N;
        cin >> N;
        for(int j=0;j<N;j++){
            c[j].index = j+1;
            cin >> c[j].D;
        }
        for(int j=0;j<N;j++){
            cin >> c[j].P;
            c[j].ratio = (double)c[j].P/c[j].D;
        }
        sort(c,c+N,cmp);
        for(int j=0;j<N;j++){
            cout << c[j].index << " ";
        }
        cout << '\n' << '\n';
    }
}