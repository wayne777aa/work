#include <bits/stdc++.h>
using namespace std;

int N,M;
int arr[1001][1001];
int dx[4] = {1,0,-1,0};
int dy[4] = {0,1,0,-1};
bool run[1001][1001] = {false};



void DFS(int x,int y){
    if(run[y][x] == true) return;
    run[y][x] = true;
    for(int i=0;i<4;i++){
        int nx = x+dx[i];
        int ny = y+dy[i];
        if(0<=nx && nx <M && 0<=ny && ny< N){
            if(run[ny][nx] == false && arr[y][x] == arr[ny][nx]){
                DFS(nx,ny);
            }
        }
    }
    return;
}


int main(){
    ios::sync_with_stdio(false); cin.tie(0); cout.tie(0);
    cin >> N >> M;
    for(int i=0;i<N;i++){
        for(int j=0;j<M;j++){
            cin >> arr[i][j];
        }
    }
    int sum=0;
    for(int i=0;i<N;i++){
        for(int j=0;j<M;j++){
            if(run[i][j] == true) continue;
            DFS(j,i);
            sum++;
        }
    }
    cout << sum;
    
    return 0;
}

/*
1 6
2 1 1 2 1 2

*/