#include <stdio.h>
#include <string.h>

typedef struct date{
    int Year;
    int Month;
    int Day;
    int count;
}Date;

int main() {
    FILE *fp,*outfp;
    Date date[10];
    int Y,M,D;
    int count = 0;

    fp = fopen("./server_log.txt", "r");
    if (fp == NULL) {
    printf("Error: Unable to open server_log.txt");
    return 0;
    }
    outfp = fopen("./log_summary.txt", "w");
    while(fscanf(fp,"%d-%d-%d", &Y,&M,&D) != EOF){
        for(int i=0;i<count+1;i++){
            if(date[i].count == 0){
                date[i].Year = Y;
                date[i].Month = M;
                date[i].Day = D;
                date[i].count++;
                count++;
                break;
            }else if(date[i].Year == Y && date[i].Month == M && date[i].Day == D){
                date[i].count++;
                break;
            }
        }
        
        int ch = 0;
        while (1) { 
            ch = fgetc(fp);
            if (ch == '\n' || ch == EOF)
                break;
        }   
    }
    for(int i=0;i<count;i++)
        fprintf(outfp, "%d-%d-%d: %d log entries\n", date[i].Year,date[i].Month,date[i].Day,date[i].count); 
    fclose(fp);
    fclose(outfp);
}