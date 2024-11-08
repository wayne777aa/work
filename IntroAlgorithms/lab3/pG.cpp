#include <bits/stdc++.h>
using namespace std;

int root[1000000];

struct Node{
    int l;
    int r;
    int weight;
};

struct cmp{
    bool operator()(Node a, Node b){
        return a.weight>b.weight; //升序
    }
};

priority_queue <Node,vector<Node>,cmp> pq;

int findroot(int a){
    return (root[a] == a)? a: (root[a] = findroot(root[a]));
}

void merge(int a, int b){
    root[findroot(a)] = findroot(b);
}

int main(){
    for(int i=0;i<1000000;i++){root[i] = i;}
    int N,M;
    cin >> N >> M;
    int u,v,w;
    Node node;
    for(int i=0;i<M;i++){
        cin >> node.l >> node.r >> node.weight;
        pq.push(node);
    }
    int k=0;
    long long sum=0;
    while(!pq.empty()){
        Node edge = pq.top();
        pq.pop();
        if(findroot(edge.l) == findroot(edge.r)) continue;
        merge(edge.l,edge.r);
        sum += edge.weight;
        k++;
    }
    if(k==N-1) cout << sum;
    else cout << -1;
    return 0;
}
/*
3 4
2 3 8
1 2 20
1 3 9
2 1 9
*/