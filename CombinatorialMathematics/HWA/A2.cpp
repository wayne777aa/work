#include <bits/stdc++.h>
using namespace std;

const int MAXN = 505;
vector<int> E[MAXN];       // 原始無向圖
vector<int> adj[MAXN];     // 左→右邊（依染色建立）
int matchR[MAXN], matchL[MAXN];;           // 右側節點的配對,左側
bool visited[MAXN];        // DFS 專用 visited
int color[MAXN];           // -1: 未染色, 0: 左集合, 1: 右集合
bool visL[MAXN], visR[MAXN]; // 找最小頂點覆蓋時用的 Z 集合標記
int n, m;

// 二分圖染色（DFS）
bool dfs_color(int u, int c) {
    color[u] = c;
    for (int v : E[u]) {
        if (color[v] == -1) {
            if (!dfs_color(v, 1 - c)) return false;
        } else if (color[v] == color[u]) {
            return false;
        }
    }
    return true;
}

// 匈牙利演算法：從左集合 u 找增廣路
bool bpm(int u) {
    for (int v : adj[u]) {
        if (visited[v]) continue;
        visited[v] = true;
        if (matchR[v] == -1 || bpm(matchR[v])) {
            matchR[v] = u;
            matchL[u] = v;
            return true;
        }
    }
    return false;
}

void dfs_cover(int u) { //找 alternating path(找出哪個)
    visL[u] = true; //篩選出有配過的左側點(但配對的已經走過(最後一個點))
    for (int v : adj[u]) {
        if (!visR[v]) {
            visR[v] = true;
            if (matchR[v] != -1 && !visL[matchR[v]]) { 
                dfs_cover(matchR[v]);
            }
        }
    }
}

int main() {
    cin >> n >> m;

    // 無向圖
    for (int i = 0; i < m; ++i) {
        int u, v;
        cin >> u >> v;
        E[u].push_back(v);
        E[v].push_back(u);
    }

    // 染色
    fill(color, color + n, -1);
    for (int i = 0; i < n; ++i)
        if (color[i] == -1)
            dfs_color(i, 0);

    // 建左→右邊
    for (int u = 0; u < n; ++u) {
        if (color[u] == 0) {
            for (int v : E[u]) {
                if (color[v] == 1)
                    adj[u].push_back(v);
            }
        }
    }

    fill(matchR, matchR + n, -1);
    fill(matchL, matchL + n, -1);
    vector<pair<int, int>> matching;
    int matchCount = 0;

    for (int u = 0; u < n; ++u) {
        if (color[u] == 0) {
            fill(visited, visited + n, false);
            if (bpm(u)) matchCount++;
        }
    }

    // 建立配對邊集合
    for (int v = 0; v < n; ++v) {
        if (matchR[v] != -1) {
            matching.emplace_back(matchR[v], v);  // 左→右
        }
    }

    // 找最小頂點覆蓋
    fill(visL, visL + n, false);
    fill(visR, visR + n, false);
    for (int u = 0; u < n; ++u) {
        if (color[u] == 0 && matchL[u] == -1) { //未被配對的L 
            dfs_cover(u);
        }
    }

    vector<int> cover;
    for (int u = 0; u < n; ++u) {
        if (color[u] == 0 && !visL[u]) cover.push_back(u);     // L - Z_L 必須選的左側點
        if (color[u] == 1 && visR[u]) cover.push_back(u);      // Z_R 必經的右側點
    }

    // 輸出最大匹配大小與邊
    cout << matchCount << "\n";
    for (auto [u, v] : matching)
        cout << u << " " << v << "\n";

    // 輸出最小頂點覆蓋大小與點
    cout << cover.size() << "\n";
    for (int u : cover)
        cout << u << " ";
    cout << "\n";

    return 0;
}
