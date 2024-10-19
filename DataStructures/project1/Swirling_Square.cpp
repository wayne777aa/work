#include <iostream>
using namespace std;

int main(){
    int n, k, round = 0;
    cin >> n;
    int arr[n][n];
    for(int i=0, j=0, count=1; count<= n*n;){
        while(j<n-round){
            arr[i][j++] = count++;
            if(count> n*n)
            break;
        }
        j--;
        i++;
        if(count> n*n)
            break;
        while(i<n-round){
            arr[i++][j] = count++;
            if(count> n*n)
            break;
        }
        i--;
        j--;
        if(count> n*n)
            break;
        while(j>=0+round){
            arr[i][j--] = count++;
            if(count> n*n)
            break;
        }
        round++;
        i--;
        j++;
        if(count> n*n)
            break;
        while(i>=0+round){
            arr[i--][j] = count++;
            if(count> n*n)
            break;
        }
        i++;
        j++;
    }
    cout << "[";
    for(int i=0;i<n;i++){
        cout << "[";
            for(int j=0;j<n;j++){
                cout << arr[i][j];
                if(j<n-1)
                    cout << ",";
            }
        cout << "]";
        if(i<n-1)
            cout << ",";
    }
    cout << "]\n";
    return 0;
}