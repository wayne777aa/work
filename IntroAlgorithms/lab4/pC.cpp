#include <bits/stdc++.h>
using namespace std;
#define IOS ios::sync_with_stdio(false);cin.tie(0);cout.tie(0);
#define LL long long

int root[300000];

int N,M;
long long coin[300000];
vector<int> A[300000]; //tunnel
vector<int> B[300000]; //reverse tunnel
vector< pair<int,LL> > fin; //<number,finishtime>
vector<int> vis(300000); //0:unvisited, 1:in prograss, 2:visited
long long room[300000]; //the number of coin in each SCC

unordered_set<long long> go[300000];
long long ans[300000];

LL DFS(int a, LL cur){
    // startime = cur
    cur++;
    vis[a] = 1; //in prograss
    for(int i=0;i<A[a].size();i++){
        if(vis[A[a][i]] == 0){
            cur = DFS(A[a][i],cur);
            cur++;
        }
        
    }
    fin[a].second = cur;
    vis[a] = 2;
    return cur;
}

void reverse(){ //reverse adjacency
    for(int i=0;i<N;i++){
        for(int j=0;j<A[i].size();j++){
            B[A[i][j]].push_back(i);
        }
    }
}

bool cmp(pair<int,LL> a,pair<int,LL> b){
    return a.second > b.second;
}

void SecondDFS(int a,vector<int> &vec){     //用&來減少複製vector
    vis[a] = 1; //in prograss
    vec.push_back(a);
    for(int i=0;i<B[a].size();i++){
        if(vis[B[a][i]] == 0){
            SecondDFS(B[a][i],vec);
        }
    }
    vis[a] = 2;
}

void findSCC(){
    for(int i=0;i<N;i++){
        if(vis[fin[i].first] == 0){ //由結束時間大到小
            vector<int> vec;
            SecondDFS(fin[i].first,vec);    //找出每個SCC 
            sort(vec.begin(), vec.end());
            LL sum=0;
            for(int j=0;j<vec.size();j++){
                sum += coin[vec[j]]; //加總SCC裡面的coin數
                root[vec[j]] = vec[0];//SCC裡最小值當root
            }
            room[vec[0]] = sum;//SCC裡的coin數
        }
    }
    return;
}

void tunnel(){//整理每個SCC能到哪裡
    for(int i=0;i<N;i++){
        for(int j=0;j<A[i].size();j++){
            go[root[i]].insert(root[A[i][j]]);
        }
    }
    for(int i=0;i<N;i++){
        go[i].erase(i); //去掉本身
    }
    return;
}

LL findans(int index){
    if(ans[root[index]] != 0) return ans[root[index]]; //因為root是取最小值 所以不用擔心有不是root的取到0
    ans[index] = room[index]; //初始化
    for (const auto &s : go[index]){ //遍歷go[index]
        ans[index] = max(ans[index],findans(s)+room[index]); //看哪條路最大值
    }
    return ans[index];
}

int main(){
    cin >> N >> M;
    
    for(int i=0;i<N;i++){
        cin >> coin[i];
        fin.push_back(make_pair(i,0));
        root[i] = i;
        ans[i] = 0;
    }
    int a,b;
    for(int i=0;i<M;i++){
        cin >> a >> b;
        A[a-1].push_back(b-1);
    }

    LL cur = 0;
    for (int i = 0; i < N; i++) {
        if (vis[i] == 0) {
            cur = DFS(i, cur);
        }
    }
    reverse();
    sort(fin.begin(),fin.begin()+N,cmp);
    fill(vis.begin(), vis.begin()+N, 0); //visit重置
    findSCC();

    tunnel();
    for(int i=0;i<N;i++){
        cout << findans(root[i]) << " ";
    }
    return 0;
}

/*
5 7
1 2 3 4 5
1 3
2 4
3 5
1 4
4 2
5 2
5 1


7 9
1 2 3 4 5 3 1
1 3
2 4
3 5
1 4
4 2
5 2
5 1
6 7
7 2

7 7
1 2 3 4 5 3 1
1 3
2 4
3 5
5 1
4 2
6 5
7 2

4 3
1000000000 1000000000 1000000000 1000000000
1 2
2 3
3 4

*/