#include <iostream>
using namespace std;
int M, N;
const int MAX = 300;
int grid[MAX][MAX];
int dx[4]={0,1,0,-1};
int dy[4]={1,0,-1,0};
void dfs(int i, int j){
    grid[i][j] = 2;
    for(int d=0; d<4; d++){
        int nx = i+dx[d];
        int ny = j+dy[d];
        if(grid[nx][ny]==1 && nx>=0 && nx<M && ny>=0 && ny<N){
            dfs(nx, ny);
        }
    }
}
int main(){
    cin >> M >> N;
    for(int i=0; i<M; i++){
        for(int j=0; j<N; j++){
            cin >> grid[i][j];
        }
    }
    int ans = 0;
    for(int i=0; i<M; i++){
        for(int j=0; j<N; j++){
            if(grid[i][j]==1){
                dfs(i, j);
                ans++;
            }
        }
    }
    cout << ans << endl;
}