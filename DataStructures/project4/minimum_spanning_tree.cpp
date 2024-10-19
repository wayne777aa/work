#include <iostream>
#include <cmath>
#include <climits>
using namespace std;

struct point{
    int x;
    int y;
    int flag = 0;
};

int main(){
    int n;
    cin >> n;
    point p[n];
    for(int i=0;i<n;i++){
        cin >> p[i].x >> p[i].y;
    }
    int sum = 0;
    p[0].flag = 1;
    for(int i=0;i<n-1;i++){
        int min = INT_MAX, minnum;
        for(int i=0;i<n;i++){ //找有接的
            if(p[i].flag != 1)
                continue;
            for(int j=1;j<n;j++){ //沒接的
                if((p[j].flag != 1) && (min > (abs(p[i].x-p[j].x)+abs(p[i].y-p[j].y)))){
                    min = (abs(p[i].x-p[j].x)+abs(p[i].y-p[j].y));
                    minnum = j;
                }
            }
        }
        sum += min;
        p[minnum].flag = 1;
    }
    cout << sum << '\n';
    return 0;
}