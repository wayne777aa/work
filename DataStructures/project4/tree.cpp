#include <iostream>
#include <algorithm>
#include <vector>
using namespace std;

struct Treenode{
    int papa;
    int val;
    int group;
};

bool cmp(Treenode a,Treenode b){
    return a.val < b.val;
}

int main(){
    int count=0;
    int pa,son;
    Treenode tree[100];
    
    while(cin >> pa >> son){
        if(pa == 0 && son == 0)
            break;
        for(int i=0;i<count;i++){
            if(son == tree[i].val){
                cout << "False" <<endl;
                return 0;
            }
        }
        tree[count].val = son;
        tree[count].papa = pa;
        tree[count].group = son;
        count++;
        
    }
    sort(tree,(tree+count),cmp);
    for(int i=0;i<count;i++){
        for(int j=0;j<count;j++){
            if(tree[i].val == tree[j].papa && tree[i].papa == tree[j].val){
                cout << "False" <<endl;
                return 0;
            }
            if(tree[i].papa == tree[j].val || tree[i].val == tree[j].papa || tree[i].papa == tree[j].papa){
                tree[j].group = tree[i].group;
            }
        }
    }

    for(int i=0;i<count;i++){
        int group = tree[0].group;
        if(group != tree[i].group){
            cout << "False" <<endl;
            return 0;
        }
    }

    cout << "True" << endl;
    return 0;
}