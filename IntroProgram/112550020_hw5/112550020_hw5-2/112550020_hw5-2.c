//島嶼類問題(DFS、BFS、DSU)
//我寫的是DSU(應該吧)自己想的


#include<stdio.h>

int main(){
    int m, i, j;
    scanf("%d", &m);
    int arr[m][m];
    int team[m];
    for(i=0; i<m ; i++){
        for(j=0 ; j<m ; j++)
            scanf("%d", &arr[i][j]);
    }

    for(i=0 ; i<m ; i++)
        team[i] = i;
    
    for(i=0; i<m ; i++){
        for(j = i+1 ; j<m ; j++){
            if(arr[i][j] == 1){
                for(int k=0 ; k<m ; k++){
                    if(team[k] == team[j]) //把同組的抓過去
                        team[k] = team[i];
                }
                team[j] = team[i]; //把對方變成自己組
            }
        }
    }

    int count[m], sum = 0;
    for(i=0;i<m;i++){
        count[i] = 0; //歸零膏
        count[team[i]] = 1; //計算幾號組有隊伍
        sum += count[i]; //計算總共幾組
    }
    printf("%d", sum);
}