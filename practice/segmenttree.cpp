//https://hackmd.io/@wiwiho/CPN-segment-tree

#include <iostream>
#include <bits/stdc++.h>
using namespace std;

int tree[4000000];//N*4
void build(int root,int l,int r){ //left right
    if(l == r){
        tree[root] = num[start];
        return;
    }
    int leftroot = root * 2+1;//左結點
    int rightroot = root * 2+2;//右結點
    int mid = (l+r)/2;
    build(leftroot,l,mid);//遞歸計算左結點
    build(rightroot,mid+1,r);//遞歸計算右結點
    tree[root] = tree[leftroot] + tree[rightroot];//根結點值=左根+右根
}