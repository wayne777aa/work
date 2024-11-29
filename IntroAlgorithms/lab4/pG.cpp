#include <bits/stdc++.h>
using namespace std;

const int M = 998244353;

int n, k;
int p;
vector<bool> block(576); //24*24=576
int dp[18][262144]; //2^18
/* to do
bool vaild[18][262144]; 
*/

long long ans;

void put(int y,int x){
    static const int dy[] = {-1,-1,-1,0,0,0,1,1,1};
    static const int dx[] = {-1,0,1,-1,0,1,-1,0,1};
    for(int i=0;i<9;i++){
        int ny = y + dy[i];
        int nx = x + dx[i];
        if(0<=nx && nx<n && 0<=ny && ny<n){
            block[ny*n+nx] = true;
        }
    }
}

bool canput(int y, int k){ //第y列 的第k種組合
    bool can = true;
    vector<bool> tmp = block;
    for(int i=0;i<n;i++){
        if((k & (1<<i))!=0){
            can = !block[y*n+i];
            if(can == false) break;
            put(y,i);
        }
    }
    block = tmp;
    return can;
}

int Permutation(int y,int k){
    if(y==n-1) return dp[y][k] = 1;
    if(dp[y][k] != 0) return dp[y][k];
    vector<bool> tmp = block;
    for(int i=0;i<n;i++){
        if((k & (1<<i))!=0)
            put(y,i);
    }
    int sum=0;
    for(int i=0;i<p;i++){
        if(canput(y+1,i)){
            sum += Permutation(y+1,i);
            sum %= M;
        }
    }
    block = tmp;
    return dp[y][k] = sum;
}


int main() {
    cin >> n >> k;
    p = pow(2,n);
    ans = 0;
    for(int i=0;i<k;i++){
        int x,y;
        cin >> x >> y;
        block[(y-1)*n+x-1] = 1;
    }
    for(int i=0;i<p;i++){ //把第0排的000...累加到111...
        if(canput(0,i) == 1)
            ans = (ans + Permutation(0,i))%M;
    }
    
    cout << ans;
    return 0;
}