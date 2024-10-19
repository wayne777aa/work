#include <iostream>
#include <bits/stdc++.h>
using namespace std;
#define INF INT_MAX

struct node{
    int go[10] = {0,0,0,0,0,0,0,0,0,0};
    int cost[11] = {INF,INF,INF,INF,INF,INF,INF,INF,INF,INF,INF}; //直接對號碼
};

node cross[11];
int parent[11];

int Dijkstra(int n,int start, int end){
    bool vis[11] = {false,false,false,false,false,false,false,false,false,false,false};
    int dis[11] = {INF,INF,INF,INF,INF,INF,INF,INF,INF,INF,INF};

    for(int i=0;i<n;i++){
        // vis[i] = false;
        dis[i+1] = cross[start].cost[i+1];
        parent[cross[start].go[i]] = start;
    }
    vis[start] = true;
    dis[start] = 0;
    for(int edge = 0;edge < n-1;edge++){ //跑n-1次
        int min = INF, nex = -1; //找最小路徑
        for(int i=1;i<=n;i++){
            if(!vis[i] && dis[i] < min){
                min = dis[i];
                nex = i;
            }
        }
        vis[nex] = true;
        for(int i=0;i<n;i++){ //更新離原點距離
            if(cross[nex].go[i] == 0){break;}
            if(!vis[cross[nex].go[i]] && dis[nex] + cross[nex].cost[cross[nex].go[i]] < dis[cross[nex].go[i]]){
                dis[cross[nex].go[i]] = dis[nex] + cross[nex].cost[cross[nex].go[i]];  
                parent[cross[nex].go[i]] = nex;
            }
        }
        if(nex == end) break; //到了終點就該結束了 沒有辦法全部路口連上
    }


    return dis[end];
}


int main(){
    int n;
    cin >> n;
    for(int i=1;i<=n;i++){
        int pathnum;
        cin >> pathnum;
        for(int j=0;j<pathnum;j++){
            cin >> cross[i].go[j] >> cross[i].cost[cross[i].go[j]];
        }
    }
    int start,end;
    cin >> start >> end;
    int dis = Dijkstra(n,start,end);

    stack<int> s;
    int now = end;
    for(int i=0;i<n;i++){
        s.push(now);
        if(now == start) break;
        now = parent[now];
    }
    cout << "Path =";
    while(!s.empty()){
        now = s.top();
        s.pop();
        cout << " " << now;
    }
    cout << "; " << dis << " second delay" << endl;
    return 0;
}