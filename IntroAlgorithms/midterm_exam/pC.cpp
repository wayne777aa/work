#include <bits/stdc++.h>
using namespace std;

int N;
bool run[100100] = {false};
struct D{
    int index;
    int dep = 0;
}dep[100010];
vector<int> vec[100010];


void DFS(int x,int de){
    if(run[x] == true) return;
    run[x] = true;
    dep[x].dep = de;
    for(int i=0;i<vec[x].size();i++){
        int np = vec[x][i];
        if(run[np] == false){
            DFS(np,de+1);
        }
    }
    return;
}

bool cmp(D a,D b){
    return a.dep > b.dep;
}

int main(){
    ios::sync_with_stdio(false); cin.tie(0); cout.tie(0);
    cin >> N;
    for(int i=0;i<N-1;i++){
        int a,b;
        cin >> a >> b;
        vec[a].push_back(b);
        vec[b].push_back(a);
        dep[i+1].index = i+1;
    }
    dep[N].index = N;
    DFS(1,0);
    sort(dep,dep+N+1,cmp);
    fill(run,run+N+1,false);
    DFS(dep[0].index,0);
    sort(dep,dep+N+1,cmp);
    cout << dep[0].dep;
    return 0;
}

/*
5
1 2
2 3
3 4
4 5

5
1 2
1 3
1 4
1 5

*/