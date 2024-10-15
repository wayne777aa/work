#include <stdio.h>
#include "game.h"

int main(){
    int lv,player;
    scanf("%d %d", &lv, &player);
    game_init(lv, player);
    game_start();
}