#include<stdio.h>
#include<string.h>

int main () {
    char ch;
    char m[40] = {0}, s[40] = {0};
    

    while(scanf("%s %s", m, s) != EOF){
        int lenm = strlen(m);
        int lens = strlen(s);
        int D = 0;

        for(int i=0, j=0; j<lens ; j++){
            if(m[i] == s[j]){
                i++;
            }
            if(i==lenm){
                D = 1;
                break;
            }
        }
        
        if(D)
            printf("Yes\n");
        else
            printf("No\n");
    }
}