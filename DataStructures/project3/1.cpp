#include <iostream>
using namespace std;

int main(){
    int N;
    cin >> N;
    int arr[N];
    for(int i=0;i<N;i++){
        cin >> arr[i];
    }
    int wait[N] = {0};
    for(int i=0;i<N-1;i++){
        int count=0;
        for(int j=i;j<N;j++){
            if(arr[i]<arr[j]){
                wait[i] = count;
                break;
            }else
                count++;
        }
    }
    for(int i=0;i<N-1;i++){
        cout << wait[i] << " ";
    }
    cout << "0" << endl;
    return 0;
}