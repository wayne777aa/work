#include <bits/stdc++.h>
using namespace std;

const int MAXN = 105;
const int INF = 1e9;

struct Edge {
    int to, rev; // rev 在對方的 adjacency list 中的 index
    int cap;
};

vector<Edge> graph[MAXN];
bool visited[MAXN];

// 加邊：無向邊 u-v 拆成 u→v 和 v→u
void add_edge(int u, int v, int c) {
    graph[u].push_back({v, (int)graph[v].size()    , c});
    graph[v].push_back({u, (int)graph[u].size() - 1, 0});  // 反向邊初始容量為 0
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
    return 0;
}
