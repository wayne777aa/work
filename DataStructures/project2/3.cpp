#include <iostream>
using namespace std;

int main(){
    int n;
    cin >> n;
    int arr[n];
    for(int i=0; i<n; i++){
        cin >> arr[i];
    }
    int count=0, t = 0;
    for(int i=0; i<n-1; i++){
        t = 0;
        for(int j=i+1; j<n; j++){
            if(t>arr[j] || t>arr[i])
                continue;
            count++;
            t = arr[j];
        }
    }
    cout << count << endl;
    return 0;
}