#include <bits/stdc++.h>
using namespace std;

int main(){
    int n,m;
    while(cin >> n >> m){
        int take[m];
        for(int i=0;i<m;i++){cin >> take[i];}

        int dp[n+1] = {0};
        for(int i=1;i<=n;i++){
            for(int j=0;j<m;j++){
                if(take[j]<=i && dp[i-take[j]] == 0) {
                    dp[i]=1;
                    break;
                }
            }
        }
        if(dp[n]==1) cout << "Stan wins\n";
        else cout << "Ollie wins\n";
    }
}