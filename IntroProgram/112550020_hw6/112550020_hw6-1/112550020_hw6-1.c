# include <stdio.h>
# include <stdbool.h>
# include <stdlib.h>
# define N 10000

typedef struct fallguy{
    int speed;
    int flexibility;
    int balance;
}fallGuy;

void swap(fallGuy *a, fallGuy *b){
    fallGuy tmp = *a;
    *a = *b;
    *b = tmp;
}

void rank(fallGuy new){
    static fallGuy rank[10000];
    static int num = 0;
    int position = num;
    int count = 0;
    rank[num] = new;
    for(int i = num; i>0 ; i--){
        if(rank[i].speed != rank[i-1].speed){
            if(rank[i].speed - rank[i-1].speed < 0)
            break;
            swap(&rank[i],&rank[i-1]);
            count++;
        }else if(rank[i].flexibility != rank[i-1].flexibility){
            if(rank[i].flexibility - rank[i-1].flexibility < 0)
            break;
            swap(&rank[i],&rank[i-1]);
            count++;
        }else if(rank[i].balance != rank[i-1].balance){
            if(rank[i].balance - rank[i-1].balance < 0)
            break;
            swap(&rank[i],&rank[i-1]);
            count++;
        }
    }
    num++;
    printf("%d ", count);
}
int main(){
    int s, f, b;
    while(scanf("%d%d%d", &s, &f, &b) != EOF){
        fallGuy new = {s,f,b};
        rank(new);
    }
    return 0;
}