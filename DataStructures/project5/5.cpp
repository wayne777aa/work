#include <iostream>
#include <bits/stdc++.h>
using namespace std;

#define INF INT_MAX/3

int dis[501][501];
int closeshopdis[501];

void floyd_warshall(int section){
    // 窮舉所有點 k 作為中間點
    for (int k=1; k<=section; k++){
        // 對每個點 k 窮舉所有點對 (i, j) 看 i -> .. -> k -> .. -> j 是否更短
        for (int i=1; i<=section; i++){
            for (int j=1; j<=section; j++){
                dis[i][j] = min(dis[i][j], dis[i][k]+dis[k][j]);
            }
        }
    }
}

int main(){
    int market,section;
    cin >> market >> section;
    int supermarket[market];
    for(int i=0;i<market;i++)
        cin >> supermarket[i];

    for(int i=1;i<=section;i++){
        for(int j=1;j<=section;j++){
            if(i == j)
                dis[i][j] = 0;
            else
                dis[i][j] = INF;
        }
    }
    int a,b, distance;
    while(cin >> a >> b){
        cin >> distance;
        dis[a][b] = distance;
        dis[b][a] = distance;
    }
    floyd_warshall(section); //找路口到路口的最短距離
    for(int i=1;i<=section;i++){
        closeshopdis[i] = INF;
    }
    for(int i=1;i<=section;i++){ //找每個路口的最近的超市距離
        for(int j=0;j<market;j++)
        if(dis[i][supermarket[j]] < closeshopdis[i]){
            closeshopdis[i] = dis[i][supermarket[j]];
        }
    }
    
    int closemax[section+1] = {0}, choose=1; //在最近距離的最大值中找最小值
    for(int k=1;k<=section;k++){        //嘗試每個路口放超市
        for(int i=1;i<=section;i++){ 
            if(dis[i][k] < closeshopdis[i]){
                if(closemax[k] < dis[i][k])
                    closemax[k] = dis[i][k];
            }else{
                if(closemax[k] <closeshopdis[i])
                    closemax[k] = closeshopdis[i];
            }
        }
    }
    for(int i=1;i<=section;i++){
        if(closemax[i] < closemax[choose])
            choose = i;
    }
    cout << choose << endl;
    return 0;
}