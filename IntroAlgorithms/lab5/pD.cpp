#include <iostream>
#include <numeric> // 用於 gcd
using namespace std;

const int MOD = 998244353;

// 快速冪模運算
long long mod_exp(long long a, long long b, long long mod) {
    long long res = 1;
    while (b > 0) {
        if (b & 1) res = res * a % mod;
        a = a * a % mod;
        b >>= 1;
    }
    return res;
}

// 計算模逆元
long long modular_inverse(long long a, long long mod) {
    return mod_exp(a, mod - 2, mod);
}

void solve(int X, int Y, int Z) {
    long long tuple_count = 0;
    long long fraction_sum = 0;

    // 枚舉所有 (a, b, c)
    for (int a = 1; a <= X; ++a) {
        for (int b = 1; b <= Y; ++b) {
            for (int c = 1; c <= Z; ++c) {
                if (gcd(a*b, c) != 1) continue; // 如果 a*b 和 c 不是互質，跳過
                ++tuple_count; // 計數
                fraction_sum += a * b * mod_exp(c, MOD - 2, MOD) % MOD; // 累加分數
                fraction_sum %= MOD;
            }
        }
    }
    cout << tuple_count << " " << fraction_sum;
    // 分數化簡為 a·b^{-1} % MOD
    return;
}

int main() {
    int X, Y, Z;
    cin >> X >> Y >> Z;

    solve(X, Y, Z);
    return 0;
}
