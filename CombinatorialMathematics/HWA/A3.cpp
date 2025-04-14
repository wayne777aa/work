#include <bits/stdc++.h>
using namespace std;

const int MAXN = 505;

int n, m;
vector<int> graph[MAXN];
int match[MAXN];        // match[v] = u 表示 v 配對到 u（雙向都會設）
int parent[MAXN];       // 用於 BFS 過程中的前驅追蹤（建構增廣路）
int base[MAXN];         // 目前節點所屬的「壓縮代表點」
bool used[MAXN];        // BFS 中是否已加入 queue
bool blossom[MAXN];     // 記錄目前哪些點在壓縮的 blossom 中
queue<int> Q;           // BFS 使用的 queue


int lca(int a, int b) {
    static bool visited[MAXN] = {};
    memset(visited, 0, sizeof(visited));
    while (true) {
        a = base[a];         // 移到當前代表點
        visited[a] = true;
        if (match[a] == -1) break;
        a = parent[match[a]];  //  交錯走法：先 match，然後往 parent 走，維持在alternating tree
    }
    while (true) {
        b = base[b];
        if (visited[b]) return b;  // 第一個碰到 visited 的就是 共同祖先(lca)
        if (match[b] == -1) break;
        b = parent[match[b]];
    }
    return -1; // 理論上不會發生
}

void mark_blossom(int v, int b, int children) { // 準備讓這些節點的 base 都變成 lca
    while (base[v] != b) {
        blossom[base[v]] = blossom[base[match[v]]] = true; //一次兩個
        parent[v] = children; //children --- v === match[v] --- 
        children = match[v];
        v = parent[match[v]];
    }
}

int find_augmenting_path(int root) {
    memset(used, 0, sizeof(used));
    memset(parent, -1, sizeof(parent));
    for (int i = 0; i < n; ++i) base[i] = i;

    Q = queue<int>();
    Q.push(root);
    used[root] = true;

    while (!Q.empty()) {
        int v = Q.front(); 
        Q.pop();
        for (int u : graph[v]) {
            if (base[v] == base[u] || match[v] == u) continue; // 忽略自環、配對對象
            if (u == root || (match[u] != -1 && parent[match[u]] != -1)) { // 遇到root || u之前配對過(走過),且match[u]也有parent(match[u]走過)
                int b = lca(v, u); // 根
                memset(blossom, 0, sizeof(blossom));
                mark_blossom(v, b, u); // v 和 u 是從兩個不同的增廣路繞回來碰撞 互相設成parent
                mark_blossom(u, b, v);
                for (int i = 0; i < n; ++i) {
                    if (blossom[base[i]]) {
                        base[i] = b;
                        if (!used[i]) {
                            used[i] = true;
                            Q.push(i);
                        }
                    }
                }
            } else if (parent[u] == -1) { // 第一次遇到的點
                parent[u] = v;
                if (match[u] == -1) return u; // 找到增廣路徑
                used[match[u]] = true;
                Q.push(match[u]);
            }
        }
    }
    return -1;
}

void augment_path(int u) { //翻轉augment_path ppv===pv---u
    while (u != -1) {
        int pv = parent[u], ppv = match[pv];
        match[u] = pv;
        match[pv] = u;
        u = ppv;
    }
}

int edmonds() {
    memset(match, -1, sizeof(match));
    int matchCount = 0;
    for (int i = 0; i < n; ++i) {
        if (match[i] == -1) {
            int u = find_augmenting_path(i);
            if (u != -1) { // 有找到
                augment_path(u);
                ++matchCount;
            }
        }
    }
    return matchCount;
}

int main() {
    cin >> n >> m;

    for (int i = 0; i < m; ++i) {
        int u, v;
        cin >> u >> v;
        graph[u].push_back(v);
        graph[v].push_back(u); // 無向邊
    }

    int matchCount = edmonds();
    cout << matchCount << "\n";

    for (int u = 0; u < n; ++u) {
        if (match[u] != -1 && u < match[u]) {
            cout << u << " " << match[u] << "\n";
        }
    }

    return 0;
}
