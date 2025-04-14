#include <bits/stdc++.h>
using namespace std;

const int MAXN = 505;
vector<int> E[MAXN];   // 原始無向圖
vector<int> adj[MAXN]; // 從左集合 u 指向右集合 v 的邊
int match[MAXN];       // 右側節點的配對
bool visited[MAXN];    // 用於每次 DFS 的 visited 記錄
int color[MAXN];       // -1 表示未染色，0 為左集合，1 為右集合
int n, m;

// 二分圖染色（DFS）
bool coloring(int u, int c) {
    color[u] = c;
    for (int v : E[u]) {
        if (color[v] == -1) {
            if (!coloring(v, 1 - c)) return false;
        } else if (color[v] == c) {
            return false; // 出現奇數環，非二分圖（但題目保證合法）
        }
    }
    return true;
}

// 匈牙利演算法：從左集合 u 找增廣路
bool bpm(int u) {
    for (int v : adj[u]) {
        if (visited[v]) continue;
        visited[v] = true;
        if (match[v] == -1 || bpm(match[v])) {
            match[v] = u;
            return true;
        }
    }
    return false;
}

int main() {
    cin >> n >> m;

    // 輸入圖（無向邊）
    for (int i = 0; i < m; ++i) {
        int u, v;
        cin >> u >> v;
        E[u].push_back(v);
        E[v].push_back(u);
    }

    // 初始化染色
    fill(color, color + n, -1);
    for (int i = 0; i < n; ++i) {
        if (color[i] == -1) {
            if (!coloring(i, 0)) {
                cerr << "Graph is not bipartite.\n";
                return 1;
            }
        }
    }

    // 根據染色結果建立左→右的配對邊
    for (int u = 0; u < n; ++u) {
        if (color[u] == 0) { // 左集合
            for (int v : E[u]) {
                if (color[v] == 1) {
                    adj[u].push_back(v);
                }
            }
        }
    }

    // 匈牙利演算法找最大匹配
    fill(match, match + n, -1);
    int matchCount = 0;
    for (int u = 0; u < n; ++u) {
        if (color[u] == 0) {
            fill(visited, visited + n, false);
            if (bpm(u)) matchCount++;
        }
    }

    cout << matchCount << "\n";
    return 0;
}