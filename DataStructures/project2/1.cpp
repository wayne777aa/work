#include <iostream>
using namespace std;

int main(){
    int n;
    cin >> n;
    int arr[n];
    for(int i=0; i<n; i++){
        cin >> arr[i];
    }
    int count = 0, re = 1;
    for(int i=1; i<n; i++){
        if(arr[i-1] > arr[i]){
            count++;
            if(re > 1 && i!=n-1){
                cout << "NO" << endl;
                return 0;
            }
        }
        if(arr[i-1] == arr[i]){
            re++;
        }else
        re = 1;
    }
        if(count > 1){
            cout << "NO" << endl;
            return 0;
        }
    cout << "YES" << endl;
    return 0;
}