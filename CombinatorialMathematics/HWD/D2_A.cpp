/* ProbId: D2-AB-Optimal-RMQ */
#include <bits/stdc++.h>
using namespace std;

vector<int> seq;
vector<vector<int>> st;

void warm_up(int s[], int n) {
    seq = vector<int>(s, s + n);
    int logn = __lg(n) + 1;
    st.assign(logn, vector<int>(n));

    for (int i = 0; i < n; ++i)
        st[0][i] = i;  // 最小值 index

    for (int k = 1; (1 << k) <= n; ++k) {
        for (int i = 0; i + (1 << k) <= n; ++i) {
            int left = st[k - 1][i];
            int right = st[k - 1][i + (1 << (k - 1))];
            st[k][i] = (seq[left] <= seq[right]) ? left : right;
        }
    }
}

int query(int l, int r) {
    if (l > r || l < 0 || r >= seq.size()) return -1;

    int k = __lg(r - l + 1);
    int left = st[k][l];
    int right = st[k][r - (1 << k) + 1];
    return (seq[left] <= seq[right]) ? seq[left] : seq[right];
}
