#include <iostream>
#include <algorithm>
using namespace std;

int main(){
    int N;
    cin >> N;
    int arr[N];
    for(int i=0;i<N;i++){
        cin >> arr[i];
    }
    int globalmax = arr[0];
    int localmax = arr[0];
    int localmin = arr[0];
    int globalmin = arr[0];
    int sum=0;
    for(int i=0;i<N;i++){
        sum += arr[i];
    }
    for(int i=1;i<N;i++){
        
        localmax = max(arr[i],localmax+arr[i]); //避免前面作負功
        localmin = min(arr[i],localmin+arr[i]);
        globalmax = max(globalmax,localmax);
        globalmin = min(globalmin,localmin);
        
    }
    int ans;
    if(sum==globalmin)
        ans = globalmax;
    else
        ans = max(globalmax,sum - globalmin);
    cout << ans << "\n";
}