#include <bits/stdc++.h>
using namespace std;

const int MAXN = 105;
const int INF = 1e9;

struct Edge {
    int to, rev; // rev 在對方的 adjacency list 中的 index
    int cap;
    bool is_real;
};

vector<Edge> graph[MAXN];
bool visited[MAXN];

// 加邊：無向邊 u-v 拆成 u→v 和 v→u
void add_edge(int u, int v, int c) {
    graph[u].push_back({v, (int)graph[v].size()    , c, 1});
    graph[v].push_back({u, (int)graph[u].size() - 1, 0, 0});  // 反向邊初始容量為 0
}

int dfs(int u, int t, int flow) {
    if (u == t) return flow; // 到終點
    visited[u] = true;
    for (Edge &e : graph[u]) {
        if (!visited[e.to] && e.cap > 0) {
            int pushed = dfs(e.to, t, min(flow, e.cap));
            if (pushed > 0) {
                e.cap -= pushed;
                graph[e.to][e.rev].cap += pushed;
                return pushed;
            }
        }
    }
    return 0;
}

int maxflow(int s, int t) {
    int flow = 0;
    while (true) {
        memset(visited, 0, sizeof(visited));
        int pushed = dfs(s, t, INF);
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
    int n, m, s, t;
    cin >> n >> m >> s >> t;
    for(int i = 0; i < m; i++) {
        int u, v, c;
        cin >> u >> v >> c;
        add_edge(u, v, c);
        add_edge(v, u, c);  // 兩邊都有cap
    }

    int flow = maxflow(s, t);
    cout << flow << endl;

    // 找 min-cut：先做 BFS 找出 s 能到達的點
    bfs_cut(s);

    // 在 visited[] 為 true 的點集 S 裡，找出所有 S → V\S 的邊
    for (int u = 0; u < n; ++u) {
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
