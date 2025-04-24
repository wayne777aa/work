#include <bits/stdc++.h>
using namespace std;

const int INF = 1e9;
int n;
int cost[505][505]; // cost[i][j] = cost of assigning i to j

int L[505], R[505], matchR[505], way[505]; //way存前一個R

int hungarian() {
    for (int i = 1; i <= n; ++i) {
        int Rcur = 0; // 目前處理的R index 0:虛擬起點節點
        matchR[Rcur] = i; //增廣路的起點
        vector<int> minv(n + 1, INF);
        vector<bool> visR(n + 1, false);

        while (true) {
            visR[Rcur] = true;
            int Lcur = matchR[Rcur], delta = INF, Rnext; // delta: 用來記錄最小 slack（若沒找到增廣路，要調整 label）

            for (int j = 1; j <= n; ++j) {
                if (!visR[j]) {
                    int cur = cost[Lcur][j] - L[Lcur] - R[j]; // cur: 距離==0 還差多少
                    if (cur < minv[j]) {
                        minv[j] = cur;
                        way[j] = Rcur; // 為了之後能 trace 回去組出完整的增廣路
                    }
                    if (minv[j] < delta) { // 找未訪問右邊點中 slack 最小的
                        delta = minv[j];
                        Rnext = j;
                    }
                }
            }

            for (int j = 0; j <= n; ++j) {
                if (visR[j]) {
                    L[matchR[j]] += delta;
                    R[j] -= delta;
                } else {
                    minv[j] -= delta;
                }
            }

            Rcur = Rnext;
            if (matchR[Rcur] == 0) break; // Rcur還沒配對
        }

        // augmenting path
        do {
            int Rnext = way[Rcur];
            matchR[Rcur] = matchR[Rnext]; //    virtualR == L -- R == L -- R == L 
            Rcur = Rnext;                 // => virtualR -- L == R -- L == R -- L
        } while (Rcur);                   // way[0]==0
    }

    // matching result in matchR[1..n], where matchR[j] = i means i matched to j
    int result = -R[0]; //-R[0]: label變化總量( == totalweight)
    cout << result << '\n';

    vector<pair<int, int>> matches(n);
    for (int j = 1; j <= n; ++j)
        matches[matchR[j] - 1] = {matchR[j] - 1, j - 1}; //matches[L's number] = {L's number, R's number}

    for (auto &[x, y] : matches)
        cout << x << ' ' << y << '\n';

    return result;
}

int main() {
    cin >> n;
    for (int i = 1; i <= n; ++i) //從 1開始 因為0要用來存起點
        for (int j = 1; j <= n; ++j)
            cin >> cost[i][j];

    hungarian();
    return 0;
}
