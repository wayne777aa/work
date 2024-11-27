#include <bits/stdc++.h>
using namespace std;
#define IOS ios::sync_with_stdio(false);cin.tie(0);cout.tie(0);

vector<int> prices(101), cafe(101), stocks(101);

int maxCaffeine(int N, int X) {
    vector<int> dp(X + 1, 0); // 初始化所有預算

    // 遍歷每種茶
    for (int i = 0; i < N; ++i) {
        int price = prices[i];
        int caffeine = cafe[i];
        int stock = stocks[i];

        // 使用二進位分解進行有限背包優化
        int count = stock;
        int k = 1;
        while (count > 0) {
            int num = min(k, count); // 拆分的數量
            int cost = num * price; // 對應的花費
            int benefit = num * caffeine; // 對應的咖啡因

            // 倒序處理以防覆蓋左上的資料
            for (int j = X; j >= cost; j--) { //窮舉用的錢(by 1, 2, 4, 8...)
                dp[j] = max(dp[j], dp[j - cost] + benefit); //取 or 不取
            }

            count -= num; // 減少剩餘數量
            k *= 2; // 翻倍
        }
    }

    return dp[X]; // 預算X的最大咖啡因攝取量
}

int main() {
    // 讀取輸入
    int N, X;
    cin >> N >> X;

    for (int i = 0; i < N; ++i) cin >> prices[i];   // 讀取每種類茶的價格
    for (int i = 0; i < N; ++i) cin >> cafe[i];     // 讀取每種類茶的咖啡因
    for (int i = 0; i < N; ++i) cin >> stocks[i];   // 讀取每種類茶的庫存

    // 計算最大咖啡因攝取量
    cout << maxCaffeine(N, X);

    return 0;
}