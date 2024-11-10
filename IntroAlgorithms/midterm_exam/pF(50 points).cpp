#include <bits/stdc++.h>
using namespace std;

int root[100010],rnk[100010];

struct Edge{
    int l;
    int r;
    double va;
    double vb;
};

int findroot(int a){
    return (root[a]==a)?a :(root[a]= findroot(root[a]));
}

void connect(int ra, int rb){
    if(rnk[ra]>rnk[rb]) swap(ra,rb);
    root[ra] = rb;
    if(rnk[ra]==rnk[rb]) rnk[rb]++;
    return;
}



bool cmp(Edge a,Edge b){
    double ratioa = a.va/a.vb;
    double ratiob = b.va/b.vb;
    return ratioa > ratiob;
}

int main(){
    ios::sync_with_stdio(false); cin.tie(0); cout.tie(0);
    int N,M;
    cin >> N >> M;
    Edge edge[M];
    for(int i=0;i<N;i++){
        root[i] = i;
        rnk[i] = 0;
    }
    for(int i=0;i<M;i++){
        cin >> edge[i].l >> edge[i].r >> edge[i].va >> edge[i].vb;
        
    }
    sort(edge,edge+M,cmp);
    double suma=0.000000,sumb=0.000000;
    for(int i=0;i<M;i++){
        int roota = findroot(edge[i].l);
        int rootb = findroot(edge[i].r);
        if(roota == rootb) continue;
        connect(roota,rootb);
        suma += edge[i].va;
        sumb += edge[i].vb;
        // sumb += 1;
    }
    cout << (double)suma/sumb;

    return 0;
}

/*
4 5
0 1 3 2
0 2 4 3
0 3 5 1
1 3 2 2
2 3 6 5


4 5
0 1 3 1
0 2 4 1
0 3 5 1
1 3 2 1
2 3 6 1

*/