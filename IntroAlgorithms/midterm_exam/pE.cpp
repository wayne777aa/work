#include <bits/stdc++.h>
using namespace std;

int arr[1000000];
int tree[4000000];

void build(int root,int l, int r){
    if(l == r){
        tree[root] = arr[l];
        return;
    }
    int lroot = root*2+1;
    int rroot = root*2+2;
    int mid = (l+r)/2;
    build(lroot,l,mid);
    build(rroot,mid+1,r);
    tree[root] = min(tree[lroot],tree[rroot]);
    return;
}

void update(int root,int l ,int r, int index, int val){
    if(l == r && l == index){
        tree[root] = val;
        return;
    }
    int lroot = root*2+1;
    int rroot = root*2+2;
    int mid = (l+r)/2;
    if(index<=mid){
        update(lroot,l,mid,index,val);
    }else if(index>mid){
        update(rroot,mid+1,r,index,val);
    }
    tree[root] = min(tree[lroot],tree[rroot]);
    return;
}

int query(int root,int l,int r, int lq, int rq){
    if(lq<=l && r <=rq) return tree[root];
    int lroot = root*2+1;
    int rroot = root*2+2;
    int mid = (l+r)/2;
    int ans = 1000100;
    if(lq<=mid){
        ans = min(ans,query(lroot,l,mid,lq,rq));
    }
    if(rq>mid){
        ans = min(ans,query(rroot,mid+1,r,lq,rq));
    }
    return ans;
}

int main(){
    ios::sync_with_stdio(false); cin.tie(0); cout.tie(0);
    int N,Q;
    cin >> N >> Q;
    for(int i=0;i<N;i++){
        cin >> arr[i];
    }
    build(0,0,N-1);
    int op,a,b;
    for(int i=0;i<Q;i++){
        cin >> op >> a >> b;
        switch (op){
            case 1:
                update(0,0,N-1,a-1,b);
                break;
            case 2:
                cout << query(0,0,N-1,a-1,b-1) << endl;
        default:
            break;
        }
        
    }
    return 0;
}

/*
10 4
4 1 10 8 8 9 3 6 10 8
2 3 7
2 4 6
2 9 10
2 2 2

9 5
9 6 1 6 6 4 6 4 2
2 7 9
1 9 6
2 7 9
1 3 8
2 1 8

*/