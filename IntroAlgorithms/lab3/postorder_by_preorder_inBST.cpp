//-------------------pB--------------------------
#include <iostream>
#include <bits/stdc++.h>
using namespace std;

struct Node{
    Node* l=0;
    Node* r=0;
    int val=0;
};
Node* root=0;
int preorder[200001],inorder[200001];
int N;
map<int, int> inorderindex;
// int inorderindex[200001];
bool flag=false;



bool cmp(int a,int b){
    return a<b;
}

Node* buildtree(int root_i,int l, int r){ //preorder_root_index, inorder_left, inorder_right
    if(l > r) return nullptr;
    if(root_i>=N || flag == true){          //invalid preorder
        flag = true;
        return nullptr;
    }
    Node* node = new Node;
    // int size_left = inorderindex[root_i];         //array
    int size_left = inorderindex[preorder[root_i]];  //map
    node -> val = preorder[root_i];
    node -> l = buildtree(root_i+1,l,size_left-1);
    node -> r = buildtree(root_i+size_left-l+1,size_left+1,r);
    return node;
}

void Postorder(Node *current){
    if(current){                               // if current != NULL
        Postorder(current->l);                 // L
        Postorder(current->r);                 // R
        cout << current->val << " ";           // V
    }
}

int BinarySearch(int tar){
    int left = 0;
    int right = N-1;
    while(left<=(N-1)){
        int mid = (left + right) /2;
        if(inorder[mid] > tar){
            right = mid-1;            
        }else if(inorder[mid] < tar){
            left = mid+1;
        }else
            return mid;
    }
    return -1;
}

int main(){
    cin >> N;
    for(int i=0;i<N;i++){
        cin >> preorder[i];
        inorder[i] = preorder[i];
    }
    sort(inorder,inorder+N,cmp);
    
    // for(int i = 0; i<N; i++){       //array
        // inorderindex[i] = BinarySearch(preorder[i]);
    // }

    for(int i = 0; i<N; i++){    //map
       inorderindex[inorder[i]] = i;
    }
    root = buildtree(0,0,N-1);
    if(flag == false)
        Postorder(root);
    else
        cout << -1;
    return 0;
}