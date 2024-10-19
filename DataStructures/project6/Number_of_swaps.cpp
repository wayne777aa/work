#include <iostream>
#include <bits/stdc++.h>
using namespace std;

int bubble_sort(int arr[], int len) {
	int i, j;
    int ans=0;
	for(i = 0; i < len - 1; i++)
		for(j = 0; j < len - 1 - i; j++)
			if(arr[j] > arr[j + 1]){
				swap(arr[j], arr[j + 1]);
                ans++;
            }
    
    return ans;
}


int main(){
    int n;
    cin >> n;
    int arr[n];
    for(int i=0;i<n;i++){
        cin >> arr[i];
    }

    cout << bubble_sort(arr,n) << endl;
    return 0;
}