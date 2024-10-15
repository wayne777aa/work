#include <iostream>
#include <bits/stdc++.h>
using namespace std;

int main(){
    int N,L;
    cin >> N >> L;
    // int count[1000000] = {0};
    int a[N],p;
    int plus[N],minus[N]; //記+1-1的位置
    for(int i=0;i<N;i++){
        cin >> a[i];
    }
    for(int i=0;i<N;i++){
        cin >> p;
        if((a[i]-1-p)>=0){ //差分 開頭+1,(結尾下一個)-1
            // count[a[i]-1-p]++;
            plus[i] = a[i]-1-p;
        }else{
            // count[0]++;
            plus[i] = 0;
        }
        if((a[i]-1+p+1)<L){
            // count[a[i]-1+p+1]--;
            minus[i] = a[i]-1+p+1;
        }else{
            // count[L]--;
            minus[i] = L;
        }
    }
    // for(int i=0;i<L;i++){
    //     count[i+1] += count[i];
    // }
    int position,numof = -1;
    sort(plus,plus+N);
    sort(minus,minus+N);
    int plusp=0,minusp=0,now=0;
    // for(int i=0;i<N;i++){
    //     if(numof<count[i]){
    //         position = i+1;
    //         numof = count[i];
    //     }
    // }
    while((plusp < N) &&(minusp < N)){
        int i=min(plus[plusp],minus[minusp]);
        while((plus[plusp] == i) && (plusp < N)){
            now++;
            plusp++;
        }
        while((minus[minusp] == i) && (minusp < N)){
            now--;
            minusp++;
        }
        if(numof < now){
            position = i+1;
            numof = now;
        }
    }
    cout << position << " " << numof;
    return 0;
}