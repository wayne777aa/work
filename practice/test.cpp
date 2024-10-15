#include <iostream>
#include <string.h>
#include <math.h>

using namespace std;
    
int main() {
    int n;
    while(cin>>n){
        for(int i=0;i<10;i++){
            float k = n-i;
            k = pow(k,2);
            k = 1000009 - k;
            k = sqrt(k);
            cout << n-i << "= " << k << "\n";
        }
    }
    return 0;
}