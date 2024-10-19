#include <iostream>  
#include <deque>  
#include <cstdlib>  
using namespace std;  
  
int main(){  
    int test, group;  
    cin >> test;  
    for(int testcase = 0; testcase < test; testcase++){  
        deque<int> d;  
        cout << "Testcase #" << testcase+1 << endl;  
        cin >> group;  
        int n[group];  
        int *arr[group];  
        for(int i=0;i<group;i++){  
            cin >> n[i]; //第i組人數  
            arr[i] = (int *) calloc(n[i], sizeof(int));  
            for(int j=0;j<n[i];j++){  
                cin >> arr[i][j];  
            }  
        }  
        int m;  
        cin >> m;  
        for(int i=0;i<m;i++){  
            string s, en("ENQUEUE"), de("DEQUEUE");  
            cin >> s;  
            if(s == en){  
                int x, ingroup = 0, flag=0;  
                cin >> x;  
  
                for(int j=0, i=0;j<group;j++){ //判斷在哪一組  
                    for(;i<n[j];){  
                        if(arr[j][i] == x){  
                            flag = 1;  
                            break;  
                        }  
                        if(flag == 1){  
                            break;  
                        }else  
                            i++;  
                    }  
                    if(flag){  
                        ingroup = j;  
                        break;  
                    }else{  
                        i = 0;  
                    }  
                }  
                int prein = 0; //前一個在不在group  
                if(flag && i!=0){  
                    int done = 0;  
                    for(int j=0; j<d.size(); j++){  
                        int in = 0, p=-1;  
                        for(int k=0; k<n[ingroup];k++){  
                            if(d[j] == arr[ingroup][k]){  
                                in = 1;  
                                break;  
                            }  
                        }  
                        if(prein == 1 && in == 0){  
                            p = j;  
                        }  
                        if(prein == 0 && in == 1){  
                            prein = 1;  
                        }  
                        if(p!=-1){  
                            auto it = d.begin();  
                            for(int i=0; i<p; i++,it++){}  
                            d.insert(it,x);  
                            done = 1;  
                            break;  
                        }  
                    }  
                    if(done == 0)  
                        d.push_back(x);  
                }else  
                    d.push_back(x);  
            }else if(s == de){  
                cout << d.front() << endl;  
                d.pop_front();  
            }  
        }  
        for(int i=0;i<group;i++)  
            free(arr[i]);  
    }  
    return 0;  
}  