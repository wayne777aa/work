#include<bits/stdc++.h>
using namespace std;

int root[100010],weight[100010],parent[100010],run[100010],dep[100010],rnk[100010];

struct Node{
    int l;
    int r;
    int w;
}node[100010];

int findroot(int a){
    return (root[a] == a)? a: (root[a] = findroot(root[a]));
}

void merge(int root_a, int root_b, int we){
    if(rnk[root_a] > rnk[root_b]) swap(root_a,root_b);
    root[root_a] = root_b;
    weight[root_a] = we;
    parent[root_a] = root_b;
    if(rnk[root_a] == rnk[root_b]) rnk[root_b]++;
}

bool cmp(Node a,Node b){
    return a.w>b.w;
}

int getdep(int cur){
	if(run[cur]){
		return dep[cur];
	}
	run[cur]=1;
	if(parent[cur]==cur){
		return dep[cur]=0;
	}else{
		return dep[cur]=1+getdep(parent[cur]);
	}
}

int main(){
    int N,M;
    cin >> N >> M;
    for(int i=0;i<=N;i++){
        root[i] = i;
        parent[i] = i;
        weight[i] = 1000000100;
        run[i] = 0;
        rnk[i] = 0;
    }
    for(int i=0;i<M;i++){
        cin >> node[i].l >> node[i].r >> node[i].w;
    }
    sort(node,node+M,cmp);
    for(int i=0;i<M;i++){
        int x = findroot(node[i].l);
        int y = findroot(node[i].r);
        int we = node[i].w;
        if(x == y) continue;
        merge(x,y,we);
    }
    for(int i=1;i<=N;i++){
        dep[i] = getdep(i);
    }
    int Q;
    cin >> Q;
    for(int i=0;i<Q;i++){
        int ll,rr,ans=1000000010;
		cin>>ll>>rr;
		int curl=ll,curr=rr;
		while(curl!=curr){
			if(dep[curl]>dep[curr]){
				ans=(ans>weight[curl])?weight[curl]:ans;
				curl=parent[curl];
			}else if(dep[curl]<dep[curr]){
				ans=(ans>weight[curr])?weight[curr]:ans;
				curr=parent[curr];
			}else{
				ans=(ans>weight[curl])?weight[curl]:ans;
				ans=(ans>weight[curr])?weight[curr]:ans;
				curl=parent[curl];
				curr=parent[curr];
			}
		}
		cout<<ans<<endl;
    }
    return 0;
}

/*
4 4
1 3 3
1 2 1
2 3 4
3 4 2
6
1 2
1 3
1 4
2 3
2 4
3 4

*/