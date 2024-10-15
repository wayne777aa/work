#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#define NUM_PLAYERS 5

    

typedef struct {
    char name[21];
    int strength;
    int luck;
} Player;

typedef struct {
    char opponent[21];
    int ratio;
} SeriesRatio;

typedef struct {
    char name[21];
    int team_id;
    Player players[NUM_PLAYERS];
    SeriesRatio series_ratio[11];
} Team;

Team *team;

void winround(int number){
    for(int i=0; i<5; i++)
        (((team+number)->players)+i)->luck = ((((team+number)->players)+i)->luck -5 +100)%100;
}

void lostround(int number){
    for(int i=0; i<5; i++)
        (((team+number)->players)+i)->luck = ((((team+number)->players)+i)->luck +5 +100)%100;
}

int Battle1(int number){
    int total0 = 0, total1 = 0;
    for(int i=0; i<5; i++){
        total0 += (((team+number)->players)+i)->strength + (((team+number)->players)+i)->luck;
    }
    for(int i=0; i<5; i++){
        total1 += (((team+number+1)->players)+i)->strength + (((team+number+1)->players)+i)->luck;
    }
    if(total0 >= total1){
        winround(number);
        lostround(number+1);
        return 0;
    }
    else{
        lostround(number);
        winround(number+1);
        return 1;   
    }
};

int Battle2(int number){
    int total0 = 0, total1 = 0;
    total0 += (((team+number)->players)+0)->strength + (((team+number)->players)+0)->luck;
    total0 += (((team+number)->players)+1)->strength + (((team+number)->players)+1)->luck;
    total0 += (((team+number)->players)+4)->strength + (((team+number)->players)+4)->luck;

    total1 += (((team+number+1)->players)+0)->strength + (((team+number+1)->players)+0)->luck;
    total1 += (((team+number+1)->players)+1)->strength + (((team+number+1)->players)+1)->luck;
    total1 += (((team+number+1)->players)+4)->strength + (((team+number+1)->players)+4)->luck;

    if(total0 >= total1){
        winround(number);
        lostround(number+1);
        return 0;
    }
    else{
        lostround(number);
        winround(number+1);
        return 1;
    }
};

int Battle3(int number){
    int total0 = 0, total1 = 0;
    total0 += (((team+number)->players)+2)->strength + (((team+number)->players)+2)->luck;
    total0 += (((team+number)->players)+3)->strength + (((team+number)->players)+3)->luck;

    total1 += (((team+number+1)->players)+2)->strength + (((team+number+1)->players)+2)->luck;
    total1 += (((team+number+1)->players)+3)->strength + (((team+number+1)->players)+3)->luck;
    if(total0 >= total1){
        winround(number);
        lostround(number+1);
        return 0;
    }
    else{
        lostround(number);
        winround(number+1);
        return 1;
    }
};

int Battle4(int number){
    int total0 = 0, total1 = 0;
    for(int i=0; i<5; i++){
        if((((team+number)->players)+i)->strength < 0)
        total0++;
    }
    for(int i=0; i<5; i++){
        if((((team+number+1)->players)+i)->strength < 0)
        total1++;
    }
    if(total0 <= total1){
        winround(number);
        lostround(number+1);
        return 0;
    }
    else{
        lostround(number);
        winround(number+1);
        return 1;
    }
};

int Battle5(int number){
    int best0_S = -1000, best0_L = 0;
    int best1_S = -1000, best1_L = 0;
    for(int i=0; i<5; i++){
        if((((team+number)->players)+i)->strength > best0_S)
        best0_S = (((team+number)->players)+i)->strength;
        if((((team+number)->players)+i)->luck > best0_L)
        best0_L = (((team+number)->players)+i)->luck;
    }
    for(int i=0; i<5; i++){
        if((((team+number+1)->players)+i)->strength > best1_S)
        best1_S = (((team+number+1)->players)+i)->strength;
        if((((team+number+1)->players)+i)->luck > best1_L)
        best1_L = (((team+number+1)->players)+i)->luck;
    }
    if((best0_S * best0_L) >= (best1_S * best1_L)){
        winround(number);
        lostround(number+1);
        return 0;
    }
    else{
        lostround(number);
        winround(number+1);
        return 1;
    }
};


int main(){
    int amount, copy_amount;
    scanf("%d", &amount);
    copy_amount = amount;
    team = (Team *)malloc(amount * (sizeof(Team)));
    for(int i=0;i<amount;i++){
        int id = 0;
        char Name[21];
        scanf("%s", Name);
        scanf("%d", &id);
        id--;
        strcpy(((team+id)->name), Name);
        ((team+id)->team_id) = id;
        for(int j=0;j<5;j++){
        scanf("%s", (((team+id)->players+j)->name));
        scanf("%d", &(((team+id)->players+j)->strength));
        scanf("%d", &(((team+id)->players+j)->luck));
        }
    }



    for(int stage = 0; amount!=1; stage++){
        for(int n=0; 2*n<amount; n++){
            int Ratio[2] = {0};
            Ratio[Battle1(2*n)]++;
            Ratio[Battle2(2*n)]++;
            Ratio[Battle3(2*n)]++;
            if(Ratio[0] != 3 && Ratio[1] != 3)
            Ratio[Battle4(2*n)]++;
            if(Ratio[0] != 3 && Ratio[1] != 3)
            Ratio[Battle5(2*n)]++;
            
            if(Ratio[0] == 3){
                strcpy(((team+2*n)->series_ratio+stage)->opponent,(team+2*n+1)->name);
                ((team+2*n)->series_ratio+stage)->ratio = Ratio[1];
                team[n] = team[2*n];

            }else{
                strcpy(((team+2*n+1)->series_ratio+stage)->opponent,(team+2*n)->name);
                ((team+2*n+1)->series_ratio+stage)->ratio = Ratio[0];
                team[n] = team[2*n+1];
            }
        }
        amount /=2;
    }

    printf("%s win from %d teams\n", team->name, copy_amount);
    for(int i=0; copy_amount!=1; i++, copy_amount /=2){
        printf("%s vs %s ", team->name, (team->series_ratio+i)->opponent);
        printf("3:%d\n", (team->series_ratio+i)->ratio);
    }
    printf("Congratulations to ");
    printf("%s", (team->players)->name);
    for(int i=1; i<5; i++)
        printf(", %s", (team->players+i)->name);
    printf(" for winning the world championship!");
    
    return 0;
}
