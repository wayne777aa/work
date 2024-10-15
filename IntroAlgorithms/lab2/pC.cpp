#include <iostream>
#include <bits/stdc++.h>
using namespace std;

bool not_prime[1000000] = {0};
void notprime(){
    not_prime[0] = true;
    not_prime[1] = true;
    for(int i=2;i<=500000;i+=2){
        if(!not_prime[i]){
            for(int j=i+i;j<=1000000;j+=i){
                not_prime[j] = true;
            }
        }   
        if(i==2) {i=1;}
    }
}

int arr[1000000];
int tree[4000000];//N*4
void build(int root,int l,int r){ //節點的left right
    if(l == r){
        if(not_prime[arr[l]] == 0)
            tree[root] = arr[l];
        else
            tree[root] = -1;
        return;
    }
    int leftroot = root*2+1;//左節點(root從0開始)的index
    int rightroot = root*2+2;//右節點的index
    int mid = (l+r)/2;
    build(leftroot,l,mid);//遞歸計算左節點(l~mid)
    build(rightroot,mid+1,r);//遞歸計算右節點(mid+1~r)

    tree[root] = max(tree[leftroot],tree[rightroot]); //取大的質數
}

int query(int root,int l,int r,int L,int R){ //查詢範圍L,R
    if(L<=l && r<=R){//都在查詢範圍內
        return tree[root]; //l~r的答案
    }
    int leftroot = root*2+1;
    int rightroot = root*2+2;
    int mid = (l+r)/2;
    int ans = -1;
    if(L<=mid){ //L在左子樹的範圍
        ans = max(ans,query(leftroot,l,mid,L,R));
    }
    if(mid<R){ //R在右子樹的範圍
        ans = max(ans,query(rightroot,mid+1,r,L,R));
    }
    return ans;
}

void update(int root,int l,int r,int index,int val){
    if(l==r && l==index){
        if(not_prime[val]==1) tree[root] = -1; //不是質數，答案=-1
        else tree[root] = val;
        return;
    }
    int leftroot = root*2+1;
    int rightroot = root*2+2;
    int mid = (l+r)/2;
    if(index<=mid){ //index在左
        update(leftroot,l,mid,index,val);
    }
    if(index>mid){ //index在右
        update(rightroot,mid+1,r,index,val);
    }
    tree[root] = max(tree[leftroot],tree[rightroot]);
    return;
}

int main(){
    notprime();
    int n,Q;
    cin >> n >> Q;
    for(int i=0;i<n;i++){
        cin >> arr[i];
    }
    build(0,0,n-1);
    int op,a,b;
    for(int i=0;i<Q;i++){
        cin >> op >> a >> b;
        switch (op){
            case 1:
                update(0,0,n-1,a-1,b);
                break;
            case 2:
                cout << query(0,0,n-1,a-1,b-1) << "\n";
                break;
        }
    }
    return 0;
}