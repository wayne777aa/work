#include <iostream>
#include <bits/stdc++.h>
using namespace std;


int n;
int num[13];
int res[6]; //restore


void dfs(int depth, int start){
    int i;
    if (depth == 6){ //輸出
    	cout << res[0];
    	for (i=1; i<6; i++)
    	{
    		cout << " " << res[i];
    	}
    	cout << "\n";
        return;
    }
    for (i=start; i<n; i++){
        // 記錄第 depth 層的選擇
    	res[depth] = num[i];
        dfs(depth+1, i+1);
    }
}

int main(){
    cin >> n;
    for(int i=0;i<n;i++){
        cin >> num[i];
    }
    sort(num,num+n-1);
    dfs(0,0);
    return 0;
}