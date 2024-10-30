#include <iostream>
#include <bits/stdc++.h>
using namespace std;
#define LL long long

int N,M;
vector<int> A[200001]; //origin adj
vector<int> B[200001]; //reverse adj
LL num[200001]; //the number of pinecones
vector< pair<int,int> > fin; //<number,finishtime>
vector<int> vis(200001); //0:unvisited, 1:in prograss, 2:visited
LL ans[200001]; //the number of pinecones in each SCC

int DFS(int a, LL cur){
    // startime = cur
    cur++;
    vis[a] = 1; //in prograss
    for(int i=0;i<A[a].size();i++){
        if(vis[A[a][i]] == 0){
            cur = DFS(A[a][i],cur);
            cur++;
        }
        
    }
    fin[a].second = cur;
    vis[a] = 2;
    return cur;
}

void reverse(){ //reverse adjacency
    for(int i=1;i<N+1;i++){
        for(int j=0;j<A[i].size();j++){
            B[A[i][j]].push_back(i);
        }
    }
}

bool cmp(pair<int,int> a,pair<int,int> b){
    return a.second > b.second;
}

void SecondDFS(int a,vector<int> &vec){//用&來減少複製vector
    vis[a] = 1; //in prograss
    vec.push_back(a);
    for(int i=0;i<B[a].size();i++){
        if(vis[B[a][i]] == 0){
            SecondDFS(B[a][i],vec);
        }
    }
    vis[a] = 2;
}

void findSCC(){
    for(int i=0;i<N;i++){
        if(vis[fin[i].first] == 0){
            vector<int> vec;
            SecondDFS(fin[i].first,vec);
            LL sum=0;
            for(int j=0;j<vec.size();j++){
                sum += num[vec[j]];
            }
            for(int j=0;j<vec.size();j++){
                ans[vec[j]] = sum;
            }
        }
    }
    return;
}

int main(){
    cin >> N >> M;
    fin.push_back(make_pair(0,0));
    for(int i=1;i<N+1;i++){
        cin >> num[i];
        fin.push_back(make_pair(i,0));
    }
    int a,b;
    for(int i=0;i<M;i++){
        cin >> a >> b;
        A[a].push_back(b);
    }
    LL cur = 0;
    for (int i = 1; i < N+1; i++) {
        if (vis[i] == 0) {
            cur = DFS(i, cur);
        }
    }
    reverse();
    sort(fin.begin(),fin.end(),cmp);
    fill(vis.begin(), vis.end(), 0);
    findSCC();
    for(int i=1;i<N+1;i++){
        cout << ans[i] << " ";
    }
    return 0;
}