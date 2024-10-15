#include <stdio.h>
#include <string.h>
#include <stdlib.h>
#define Max_nameline 20

typedef struct meow{
    char name[21];
    int count;
}Meow;

int read_line(Meow *str,int n){
    char cat[Max_nameline+1];
    int ch, count = 0;
    while(1){
        ch = getchar();
        if(('A'<=ch&&ch<='Z')||('a'<=ch&&ch<='z'))
            cat[count++] = ch;
        else if((count == 0)&&(ch == EOF)) 
            return EOF;
        else if((count == 0)&&(ch == '\n' || ch == ' '))
            continue;
        else if(ch == '\n' || ch == ' ' || ch == EOF)
            break;
        else
            continue;
    }
    cat[count] = 0;
    for(int i=0; ;i++){
        if(str[i].count == 0){
            strcpy(str[i].name,cat);
            str[i].count++;
            break;
        }else if(strcmp(str[i].name,cat) == 0){
            str[i].count++;
            break;
        }
    }
    return count;
}

int main(){
    Meow *army;
    army = calloc(250,sizeof(Meow));
    while(read_line(army, Max_nameline) != EOF);
    for(int i=0, last=251, big;i<5;i++){
        big = 0;
        for(int j=0;;j++){
            if(army[j].count == 0)
                break;
            else if(army[j].count == -1){
                if(army[big].count == -1)
                    big++;
                continue;
                
            }
            if(army[j].count > army[big].count && army[j].count <= last){
                big = j;
            }else if(army[j].count == army[big].count){
                if(strlen(army[j].name) > strlen(army[big].name))
                    big = j;
            }
        }
        printf("%s %d\n", army[big].name, army[big].count);
        last = army[big].count;
        army[big].count = -1;
        
    }
    return 0;
}