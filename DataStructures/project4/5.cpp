#include <iostream>
#include <cstdlib>
#include <algorithm>
using namespace std;

struct Node{
    int apple;
    int papa = -1;
    int d;
    int son[10000];
};

bool cmp(int a,int b){
    return a > b;
}

int main(){
    
    int n;
    cin >> n;
    Node tree[n];
    int v,apple,d;
    for(int i=0;i<n;i++){
        cin >> v >> apple >> d;
        tree[v-1].apple = apple;
        tree[v-1].d = d;
        for(int j=0;j<d;j++){
            int num;
            cin >> num;
            tree[num-1].papa = v-1;
            tree[v-1].son[j] = num-1;
        }
    }
    int root;
    for(int i=0;i<n;i++){
        if(tree[i].papa == -1){
            root = i;
            break;
        }
    }
    int count=0;
    while(tree[root].apple != 1 || tree[root].d != 0){
        for(int i=0;i<n;i++){
            if(tree[i].d==0 ){
                int a=tree[i].apple-1;
                tree[i].apple-=a;
                tree[tree[i].papa].apple+=a;
                count+=abs(a);
                for(int j=0;j<tree[tree[i].papa].d;j++){
                    if((tree[tree[i].papa].son[j]) == i){
                        tree[tree[i].papa].son[j] = -1;
                        sort(tree[tree[i].papa].son,(tree[tree[i].papa].son)+tree[tree[i].papa].d,cmp);
                        tree[tree[i].papa].d--;
                    }
                }
            }
        }
    }
    cout << count << endl;
    return 0;
}