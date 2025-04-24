#include <bits/stdc++.h>
using namespace std;

const int INF = 1e9;
int n;
int cost[105][105];  // weight matrix
int matchL[105], matchR[105];
bool visL[105], visR[105];
int slack[105];
int lx[105], ly[105];

bool dfs(int u) {
    visL[u] = true;
    for (int v = 0; v < n; ++v){
        if (visR[v]) continue;
        int gap = cost[u][v] - lx[u] - ly[v];
        if (gap == 0){ // gap == 0:「等邊」。兩端點的點權重相加，恰好等於邊權重。進行擴充。
            visR[v] = true;
            if (matchR[v] == -1 || dfs(matchR[v])) { //右邊的點沒有配對 || 右邊的點配對的點可以換人配對
                matchL[u] = v;
                matchR[v] = u;
                return true;
            }
        }else{ // 找不到等邊 調整差值slack
            if (gap < slack[v]){
                slack[v] = gap;
            }
        }
    }
    return false;
}

void update_labels(){
    int delta = INF;
    for (int v = 0; v < n; ++v){
        if (!visR[v]) // 未訪問的點(gap != 0)
            delta = min(delta, slack[v]); // 最小差值slack
    }

    if (delta == INF) return;

    for (int i = 0; i < n; ++i){
        if (visL[i]) lx[i] += delta; // 偶點-delta
        if (visR[i]) ly[i] -= delta; // 奇點+delta
    }
    for (int v = 0; v < n; ++v){
        if (!visR[v])
            slack[v] -= delta;
    }
}

void hungarian() {
    memset(matchL, -1, sizeof(matchL));
    memset(matchR, -1, sizeof(matchR));
    memset(lx, 0, sizeof(lx));
    memset(ly, 0, sizeof(ly));

    for (int u = 0; u < n; ++u){
        fill(slack, slack + n, INF);

        while (true){
            fill(visL, visL + n, false);
            fill(visR, visR + n, false);
            if (dfs(u)) break;
            update_labels();
        }
    }

    int total_cost = 0;
    for (int u = 0; u < n; ++u)
        total_cost += cost[u][matchL[u]];

    cout << total_cost << '\n';
    for (int u = 0; u < n; ++u)
        cout << u << ' ' << matchL[u] << '\n';
}

int main() {
    cin >> n;
    for (int i = 0; i < n; ++i)
        for (int j = 0; j < n; ++j)
            cin >> cost[i][j];

    hungarian();
    return 0;
}
