#include <bits/stdc++.h>
using namespace std;
#define IOS ios::sync_with_stdio(false);cin.tie(0);cout.tie(0);

int LCS(int n,int m){
    char s1[n],s2[m];
    for(int i=0;i<n;i++){
        cin >> s1[i];
    }
    for(int i=0;i<m;i++){
        cin >> s2[i];
    }
    int length[n+1][m+1];
	// 初始值：當s1或s2是空集合，則LCS是空集合。
	for (int i=0; i<=n; i++) length[i][0] = 0;
	for (int j=0; j<=m; j++) length[0][j] = 0;

	// 填表格：依照遞迴公式
	for (int i=0; i<n; i++)
		for (int j=0; j<m; j++)
			if (s1[i] == s2[j])
				length[i+1][j+1] = length[i][j] + 1;
			else
				length[i+1][j+1] = max(length[i+1][j],
								   length[i][j+1]);

	return length[n][m];
}


int main(){
    IOS
    int k;
    cin >> k;
    for(int i=0;i<k;i++){
        int n, m;
        cin >> n >> m;
        cout << LCS(n,m) << endl;
    }
}