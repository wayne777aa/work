#include <iostream>
using namespace std;

int main(){
    int n;
    cin >> n;
    int arr[n][n];
    for(int i=0;i<n;i++){
        for(int j=0;j<n;j++){
            cin >> arr[i][j];
        }
    }
    int sum = 0, max = 0;
    for(int i=0;i<n;i++){ //決定哪一個起始
        for(int j=0;j<n;j++){
            for(int k=0;(i+k)<n;k++){ //決定幾乘幾
                for(int l=0;(j+l)<n;l++){
                    for(int x=0;x<=k;x++){
                        for(int y=0;y<=l;y++){
                            sum += arr[i+x][j+y];
                        }
                    }
                if(sum > max)
                max = sum;
                sum = 0;
                }
            }
        }
    }
    cout << max << endl;
    return 0;
}