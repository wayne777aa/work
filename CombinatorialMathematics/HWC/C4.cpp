#include <bits/stdc++.h>
using namespace std;

const int MAXN = 505;
const long long INF = (long long)1e18;

struct Edge {
    int to, rev; // rev 在對方的 adjacency list 中的 index
    long long cap;
    bool is_real;
};

vector<Edge> graph[MAXN];
bool visited[MAXN];
int parent[MAXN]; //用來記錄 BFS 過程中如何走回增廣路（建路徑用）
int edge_idx[MAXN];

// 加邊：無向邊 u-v 拆成 u→v 和 v→u
void add_edge(long long u, long long v, long long c) {
    graph[u].push_back({v, (int)graph[v].size()    , c, 1});
    graph[v].push_back({u, (int)graph[u].size() - 1, 0, 0});  // 反向邊初始容量為 0
}

long long bfs(int s, int t) {
    queue<int> q;
    q.push(s);
    visited[s] = true;
    parent[s] = -1;

    while (!q.empty()) {
        int u = q.front(); q.pop();
        for (size_t i = 0; i < graph[u].size(); i++) {
            Edge &e = graph[u][i];
            if (!visited[e.to] && e.cap > 0) {
                visited[e.to] = true;
                parent[e.to] = u;
                edge_idx[e.to] = i;
                if (e.to == t) {
                    // 找最大flow
                    long long flow = INF;
                    int cur = t;
                    while (cur != s) {
                        int prev = parent[cur];
                        Edge &ed = graph[prev][edge_idx[cur]]; // edge_idx[cur]: prev to cur 的邊在 graph[prev] 中的 index
                        flow = min(flow, ed.cap);
                        cur = prev;
                    }
                    // 增減正向邊和反向邊
                    cur = t;
                    while (cur != s) {
                        int prev = parent[cur];
                        Edge &ed = graph[prev][edge_idx[cur]];
                        ed.cap -= flow;
                        graph[ed.to][ed.rev].cap += flow;
                        cur = prev;
                    }
                    return flow;
                }
                q.push(e.to);
            }
        }
    }
    return 0;
}

long long maxflow(int s, int t) {
    long long flow = 0;
    while (true) {
        memset(visited, 0, sizeof(visited));
        long long pushed = bfs(s, t);
        if (pushed == 0) break;
        flow += pushed;
    }
    return flow;
}

void bfs_cut(int s) { // 分 S 和 V/S
    memset(visited, 0, sizeof(visited)); // 用於歸類屬於S的
    queue<int> q;
    visited[s] = true;
    q.push(s);
    while (!q.empty()) {
        int u = q.front(); q.pop();
        for (Edge &e : graph[u]) {
            if (e.cap > 0 && !visited[e.to]) { // 只要還有cap 就不是min cut要找的 直接加入S那區
                visited[e.to] = true;
                q.push(e.to);
            }
        }
    }
}

int main() {
    long long n, m, s, t;
    cin >> n >> m >> s >> t;
    for(int i = 0; i < m; i++) {
        long long u, v, c;
        cin >> u >> v >> c;
        add_edge(u, v, c);
        add_edge(v, u, c);  // 兩邊都有cap
    }

    long long flow = maxflow(s, t);
    cout << flow << endl;

    // 找 min-cut：先做 BFS 找出 s 能到達的點
    bfs_cut(s);

    // 在 visited[] 為 true 的點集 S 裡，找出所有 S → V\S 的邊
    for (int u = 0; u < n; u++) {
        if (visited[u]) {
            for (Edge &e : graph[u]) {
                if (!visited[e.to] && graph[e.to][e.rev].cap > 0) {
                    if(e.is_real)
                        cout << u << " " << e.to << endl;
                }
            }
        }
    }

    return 0;
}
