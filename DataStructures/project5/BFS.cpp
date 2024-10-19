#include <iostream>
#include <bits/stdc++.h>
using namespace std;

struct node{
    int x,y,z,step;
};

int L,R,C;
char maze[30][30][30]; //LRC,zyx
bool vis[30][30][30];
node s,e;
int dx[6]={1,0,-1,0,0,0},dy[6]={0,1,0,-1,0,0},dz[6]={0,0,0,0,1,-1};

bool judge(int z,int y,int x){
    if(z>=0&&z<L && y>=0&&y<R && x>=0&&x<C && maze[z][y][x]!='#' && vis[z][y][x] == false) return true;
    return false;
}

int bfs(){
    queue<node> q;
    q.push(s);
    vis[s.z][s.y][s.x]= true;
    while(q.size()){
        node now = q.front();
        vis[now.z][now.y][now.x] = true;
        q.pop();
        for(int i=0;i<6;i++){
            node next;
            next.x = now.x + dx[i];
            next.y = now.y + dy[i];
            next.z = now.z + dz[i];
            if(judge(next.z,next.y,next.x)){
                next.step = now.step+1;
                q.push(next);
            }
            if(next.x == e.x && next.y == e.y && next.z == e.z){
                return next.step;
            }
        }
    }
    return -1;
}

int main(){
    cin >> L >> R >> C;
    for(int floor=0;floor<L;floor++){
        for(int row=0;row<R;row++){
            for(int column=0;column<C;column++){
                cin >> maze[floor][row][column];
                if(maze[floor][row][column] == 'S'){
                    s.x = column;
                    s.y = row;
                    s.z = floor;
                    s.step = 0;
                }
                if(maze[floor][row][column] == 'E'){
                    e.x = column;
                    e.y = row;
                    e.z = floor;
                }
            }
        }
    }
    int ans = bfs();
    if(ans!=-1)
    cout << "Escaped in " << ans << " minute(s)." << endl;
    else 
    cout << "Trapped!" << endl;
    return 0;
}