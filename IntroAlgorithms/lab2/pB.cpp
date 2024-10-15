#include <iostream>
#include <bits/stdc++.h>
using namespace std;
const int Mod = 1e9+7;

//--------------------矩陣乘法------------------------
vector<vector<long long>> matrixmul(vector<vector<long long>> a,vector<vector<long long>> b){
    vector<vector<long long>> c = {{0,0,0,0},{0,0,0,0},{0,0,0,0},{0,0,0,0}};
    for(int i=0;i<4;i++){
        for(int j=0;j<4;j++){
            for(int k=0;k<4;k++){
                c[i][j] = (c[i][j] + a[i][k] * b[k][j]) % Mod;
            }
        }
    }
    return c;
}
//----------------矩陣次方---------------------
vector<vector<long long>> matrix_pow(vector<vector<long long>> x,long long n) {
    if (n == 1) return x;
  
    // 如果 n = 2k (偶數)
    // 則 x^n = (x^k) * (x^k)
    if (n % 2 == 0) {
        vector<vector<long long>> xk = matrix_pow(x, n/2);
        return matrixmul(xk,xk);
    }
  
    // 如果 n = 2k + 1 (奇數)
    // 則 x^n = x * (x^k) * (x^k)
    vector<vector<long long>> xk = matrix_pow(x, (n-1)/2);
    return matrixmul(matrixmul(x,xk),xk);
}

int main(){
    int k,s;
    cin >> k >> s;
    long long x1,x2,a,b,c,n;
    for(int i=0;i<k;i++){
        cin >> x1 >> x2 >> a >> b >> c >> n;
        vector<vector<long long>> arr = {
            {a , b , c , 0},
            {1 , 0 , 0 , 0},
            {0 , 0 , 1 , 0},
            {1 , 0 , 0 , 1}
        }; //列 行
        vector<long long> initial = {
            x2,
            x1,
            1,
            x1 //Sn (n=1)
        };
        vector<vector<long long>> matrix = matrix_pow(arr,n-2);
        long long An = (matrix[0][0] * x2 + matrix[0][1] * x1 + matrix[0][2])% Mod;
        long long Sn = 0;
        if(s==1){
            Sn = ((matrix[3][0]*initial[0])% Mod +(matrix[3][1]*initial[1])% Mod+(matrix[3][2]*initial[2])% Mod+(matrix[3][3]*initial[3])% Mod)% Mod;
            Sn = (Sn+An)% Mod;
        }
        cout << An << " " << Sn*s << "\n";
    }
    return 0;
}