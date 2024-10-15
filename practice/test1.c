# include <stdio.h>
# include <string.h>
#define print(n) printf( #n"= %d\n",n)


int main(){
    int i =1, j=2;
    char str[20] = "abcd";
    print(i+j);
}