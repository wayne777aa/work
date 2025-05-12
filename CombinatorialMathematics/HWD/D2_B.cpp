/* ProbId: D2-AB-Optimal-RMQ */
#include <bits/stdc++.h>
using namespace std;

const int S = 9; // Optimal block size

vector<int> seqdata;
vector<int> block_mins;
vector<int> block_mins_index;
vector<vector<int>> sparse;
unordered_map<int, vector<vector<int>>> block_lookup;

void warm_up(int seq[], int n) {
    seqdata.assign(seq, seq + n); //複製seq
    int blocks = (n + S - 1) / S; //block數

    // Block minima (value & index)
    block_mins.resize(blocks);
    block_mins_index.resize(blocks);

    for (int b = 0; b < blocks; ++b) { //暴力找最小值 並紀錄index
        int l = b * S, r = min(n, (b + 1) * S);
        int min_val = seq[l], min_idx = l;
        for (int i = l + 1; i < r; ++i) {
            if (seq[i] < min_val) min_val = seq[i], min_idx = i;
        }
        block_mins[b] = min_val;
        block_mins_index[b] = min_idx;
    }

    // Sparse Table on block_mins
    int logn = 32 - __builtin_clz(blocks); //找floor(log2(x))
    sparse.assign(logn, vector<int>(blocks));
    for (int i = 0; i < blocks; ++i) sparse[0][i] = i; // sparse[k][i]: 代表區間 [i, i + (1<<k) - 1] 的最小值是哪個 block

    for (int k = 1; (1 << k) <= blocks; ++k) {
        for (int i = 0; i + (1 << k) <= blocks; ++i) { 
            int l = sparse[k - 1][i], r = sparse[k - 1][i + (1 << (k - 1))];
            sparse[k][i] = (block_mins[l] <= block_mins[r] ? l : r);
        }
    }
}

int query(int left, int right) {
    if (left > right || left < 0 || right >= (int)seqdata.size()) return -1;

    int bl = left / S, br = right / S;

    int min_idx = left;

    // Left partial block
    int le = min((bl + 1) * S - 1, right); //避免在只有一塊時 超出right
    for (int i = left; i <= le; ++i)
        if (seqdata[i] < seqdata[min_idx]) min_idx = i;

    // Right partial block
    if (bl != br) {
        int rs = br * S;
        for (int i = rs; i <= right; ++i)
            if (seqdata[i] < seqdata[min_idx]) min_idx = i;
    }

    // Middle blocks via sparse table
    if (bl + 1 <= br - 1) {// 有中間塊
        int len = br - bl - 1;
        int k = 31 - __builtin_clz(len);
        int left_blk = sparse[k][bl + 1], right_blk = sparse[k][br - (1 << k)];
        int cand_blk = (block_mins[left_blk] <= block_mins[right_blk]) ? left_blk : right_blk;
        if (block_mins[cand_blk] < seqdata[min_idx])
            min_idx = block_mins_index[cand_blk];
    }

    return seqdata[min_idx];
    // return min_idx;
}
