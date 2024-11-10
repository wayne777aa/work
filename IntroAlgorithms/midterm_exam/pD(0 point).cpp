#include <bits/stdc++.h>
using namespace std;
const int Mod = 1e9+7;

vector<vector<long long>> matmul(vector<vector<long long>> mat1,vector<vector<long long>> mat2){
    vector<vector<long long>> sum = {
            {0,0,0,0},
            {0,0,0,0},
            {0,0,0,0},
            {0,0,0,0}
        };
    
    for(int i=0;i<4;i++){
        for(int j=0;j<4;j++){
            long long s=0;
            for(int k=0;k<4;k++){
                s += mat1[i][k]*mat2[k][j] % Mod;
            }
            sum[i][j] = s;
        }
    }
    return sum;
}

vector<vector<long long>> squ(vector<vector<long long>> mat,long long n){
    if(n==1) return mat;
    if(n%2 ==0){
        vector<vector<long long>> a = squ(mat,n/2);
        return matmul(a,a);
    }else{
        vector<vector<long long>> a = squ(mat,n/2);
        return matmul(matmul(a,a),mat);
    }
}


int main(){
    ios::sync_with_stdio(false); cin.tie(0); cout.tie(0);
    int k,s;
    cin >> k >> s;
    for(int i=0;i<k;i++){
        long long x1,x2,a,b,c,d,n;
        cin >> x1 >> x2 >> a >> b >> c >> d >> n;
        vector<long long> orig = {x1*d+x2,x2,x1,0};
        vector<vector<long long>> mat = {
            {d,a,b,c},
            {0,a,b,c},
            {0,1,0,0},
            {0,0,1,0}
        };
        vector<vector<long long>> sum = squ(mat,n-2);
        long long Sn = (sum[0][0]*orig[0]) %Mod+ (sum[0][1]*orig[1]) %Mod+ (sum[0][2]*orig[2]) %Mod+ (sum[0][3]*orig[3]) %Mod;
        long long Xn = (sum[1][0]*orig[0]) %Mod+ (sum[1][1]*orig[1]) %Mod+ (sum[1][2]*orig[2]) %Mod+ (sum[1][3]*orig[3]) %Mod;
        cout << Xn << " " << Sn*s << '\n';
    }
    return 0;
}

/*
x1 x2 a b c d n
3 1
1 1 1 1 0 1 3
1 1 1 1 0 1 4
1 1 1 1 0 2 4



2 0
1 1 4 0 0 1 10
1 2 2 0 0 1 5

*/