#include <bits/stdc++.h>
using namespace std;
#define IOS ios::sync_with_stdio(false);cin.tie(0);cout.tie(0);

const int INF = 300000;
int low[200010];
int N, length;

unordered_set<long long> go[200010];
int ans[200010];

struct Mons{
    int d;
    int v;
    int l;
}mons[200010];

int binary_search(int *a, int R, int x){ //返回第一個比x大的index(最接近x的較大值)
    int L = 0, mid;
    while(L <= R){
        mid = (L+R) >> 1;
        if(a[mid] < x)
            L = mid + 1;
        else 
            R = mid - 1;
    }
    return L;
}

int findans(int index){
    if(ans[index] != 0) return ans[index]; //因為root是取最小值 所以不用擔心有不是root的取到0
    ans[index] = mons[index].v; //初始化
    for (const auto &s : go[index]){ //遍歷go[index]
        ans[index] = max(ans[index],findans(s)+mons[index].v); //看哪條路最大值
    }
    return ans[index];
}

int main(){
    cin >> N;

    for(int i=0; i<N; i++) {
        cin >> mons[i].d >> mons[i].v >> mons[i].l;
        low[i] = INF;
        if(N<=5000)
            for(int j=i-1;j>=i-mons[i].l;j--){
                if(mons[j].d<mons[i].d)
                    go[j].insert(i);
            }
    }

    if(N<=5000){
        int maxi=0;
        for(int i=0;i<N;i++){
            maxi = max(maxi,findans(i));
        }
        cout << maxi;
    }else{ //LIS(with binary_search)
        low[0] = mons[0].d;
        length = 0;
        for(int i=1; i<N; i++){
            if(mons[i].d > low[length])
                low[++length] = mons[i].d;
            else
                low[binary_search(low, length, mons[i].d)] = mons[i].d;
        }
        cout << length+1;
    }
    return 0;
}

/*
5
3 1 0
4 1 1
1 1 2
4 1 3
5 1 4

5
5 1 0
3 1 1
1 1 2
1 1 3
5 1 4

*/