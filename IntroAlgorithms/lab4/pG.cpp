#include <bits/stdc++.h>
using namespace std;

const int M = 998244353;

int n, k;
bitset<576> block; //24*24=576
// bitset<576> king;
long long ans;

void put(int y,int x){
    static const int dy[] = {-1,-1,-1,0,0,0,1,1,1};
    static const int dx[] = {-1,0,1,-1,0,1,-1,0,1};
    for(int i=0;i<9;i++){
        int ny = y + dy[i];
        int nx = x + dx[i];
        if(0<=nx && nx<n && 0<=ny && ny<n){
            block.set(ny*n+nx);
        }
    }
}

void backtrack(int y,int x){
    int pos = y*n+x;
    ans++;
    ans %= M;
    if(pos==n*n) return;
    for(int i=pos;i<n*n;i++){
        if(block[i]==0){
            bitset<576> tmp = block;
            // king.set(i);
            put(i/n,i%n);
            backtrack(i/n,i%n);
            block = tmp;
            // king.reset(i);
        }
    }
}


int main() {
    cin >> n >> k;
    
    ans = 0;
    block.reset();
    // king.reset();
    for(int i=0;i<k;i++){
        int x,y;
        cin >> x >> y;
        block.set((y-1)*n+x-1);
    }
    backtrack(0,0);
    cout << ans;
    return 0;
}