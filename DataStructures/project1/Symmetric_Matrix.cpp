#include <iostream>
using namespace std;

int main(){
    int T;
    cin >> T;
    int n;
    for(int i=0;i<T;i++){
        cin >> n;
        int arr[n][n];
        for(int i=0;i<n;i++){
            for(int j=0;j<n;j++){
                cin >> arr[i][j];
            }
        }
        int flag = 0;
        for(int i=0;i<n;i++){
            for(int j=0;j<n;j++){
                if(arr[i][j]!=arr[j][i])
                    flag = 1;
            }
        }
        if(flag)
            cout << "Test #" << i+1 << ": Non-symmetric." << endl;
        else
            cout << "Test #" << i+1 << ": Symmetric." << endl;
    }
    return 0;
}