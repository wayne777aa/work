#include <iostream>
#include <bits/stdc++.h>
using namespace std;

bool flood[1000][1000];
int school[1000][1000];
int dx[4] = {0, 1, 0, -1};
int dy[4] = {1, 0, -1, 0};
int n, m;

bool bfs(int i, int j) {
    queue<pair<int, int>> q;
    q.push({i, j});
    bool isolated = true;
    while (!q.empty()) {
        int x = q.front().second;
        int y = q.front().first;
        q.pop();
        if (flood[y][x]) continue;
        flood[y][x] = true;
        for (int d=0; d<4; d++) {
            int nx = x + dx[d];
            int ny = y + dy[d];
            if (nx >= 0 && nx < m && ny >= 0 && ny < n) {
                if (school[ny][nx] > school[y][x]) {
                    isolated = false;
                } else if (school[ny][nx] == school[y][x] && !flood[ny][nx]) {
                    q.push({ny, nx});
                }
            }
        }
    }
    return isolated;
}

int main() {
    cin >> n >> m;
    int sum = 0;
    for (int i=0; i<n; i++) {
        for (int j=0; j<m; j++) {
            cin >> school[i][j];
        }
    }
    for (int i=0; i<n; i++) {
        for (int j=0; j<m; j++) {
            if (!flood[i][j] && bfs(i, j)) {
                sum++;
            }
        }
    }
    cout << sum << endl;
    return 0;
}