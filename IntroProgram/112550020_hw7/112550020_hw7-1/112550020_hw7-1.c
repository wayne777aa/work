#include <stdio.h>
#include <string.h>
#include <stdlib.h>
#include <assert.h>
#define MSG_len 310+1

char answer[MSG_len+1] = {0};
int len_answer = 0;

int read_line(char str[], int n) {
    int ch, i = 0;
    while (1) { 
        ch = getchar();
        if (ch == '@' || ch == EOF)
            break;
        if(ch == ',') //避免輸入到','
            continue;
        if (i < n)
            str[i++] = ch;
    }
    str[i] = '\0';
    return i;
}

void reverse(char *message, int len) {
    char temp = *message;
    char *p = message + len-1;
    for(int i=0; i<len/2; i++) {
        temp = *message;
        *message++ = *p;
        *p-- = temp;
    }
}

void plus(char num_1[],char num_2[]){
    static int i=0;
    int a = (int)num_1[0] - '0', b = (int)num_2[0] - '0';
    if(a<0)
    a = 0;
    if(b<0)
    b = 0;
    answer[i] += a+b;
    if(answer[i] >= 10){
        answer[i+1] += 1;
        answer[i] -= 10;
        if(i+1>len_answer-1) //原長度310 i只會跑到309 所以len_answer要-1
            len_answer++;
    }
    i++;
}

int max(int a, int b){
    if(a>=b)
        return a;
    else
        return b;
}

int main(){
    char ch1[31] = {0}, ch2[31] = {0};
    char number_1[MSG_len] = {0}, number_2[MSG_len] = {0};
    int len1, len2;
    int x1, x2;

    len1 = read_line(ch1,31);
    scanf("%d", &x1);
    len1 = len1*x1;
    getchar();
    len2 = read_line(ch2,31);
    scanf("%d", &x2);
    len2 = len2*x2;
    for(int i=0; i< x1; i++)
        strcat(number_1, ch1);
    for(int i=0; i< x2; i++)
        strcat(number_2, ch2);
    

    if(ch1[0] == '0'){ //避免出現00
        for(int i=1; i<len1; i++)
            number_1[i] = 0;
            len1 = 1;
    }
    if(ch2[0] == '0'){
        for(int i=1; i<len2; i++)
            number_2[i] = 0;
            len2 = 1;
    }
    len_answer = max(len1,len2);

    for(int i=len1-1,j=len2-1; i>=0 || j>=0; i--,j--){ //把兩數相加
        static char null[1] = {0};
        if(i<0){
            plus(&null[0], &number_2[j]);
            continue;
        }
        if(j<0){
            plus(&number_1[i], &null[0]);
            continue;
        }
        plus(&number_1[i], &number_2[j]);
    }

    for(int i=0; i<len_answer;i++) //我直接用數字 最後要在加'0'
        answer[i] += '0';
    reverse(answer, strlen(answer)); //我由前到後加，最後要反轉，輸出才正確

    int count = 1, A = 1;
    for(int i=0,j; A<=len_answer ; A++, count = 1, i = 0){
        j = A;
        while(j < len_answer && len_answer%A == 0){
            if(strncmp(&answer[i],&answer[j],A) == 0){
                i += A;
                j += A;
                count++;
            }else
                break;
        }

        if(j >= len_answer)
            break;
        
    }

    for(int i=0; i<A && i<len_answer ; i++){
        if((i-(A%3))%3 == 0 && i != 0)
            printf(",");
        printf("%c", answer[i]);
    }
    printf("@");
    printf("%d", count);

    return 0;
}