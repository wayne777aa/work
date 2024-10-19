#include <iostream>
using namespace std;

int main(){
    int n;
    cin >> n;
    int arr[n];
    for(int i=0; i<n; i++){
        cin >> arr[i];
    }
    int t=arr[0];
    for(int i=1;i<n;i++){
        if(arr[i-1]<arr[i] && arr[i-1]<t && arr[i]<t){
            cout << "NO" << endl;
            return 0;
        }
        if(arr[i] > t){
            t = arr[i];
        }
    }
    cout << "YES" << endl;
    return 0;
}