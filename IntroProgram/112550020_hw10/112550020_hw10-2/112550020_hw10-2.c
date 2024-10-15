#include <stdio.h>
int main(){
    int b,m,ans;
    scanf("%d%d",&b,&m);
    if( (m == 1 && b == 4 ) || (b < m) ) {
		printf("monkeys QQ\n");
		return 0;
	}
    // To do /////////////
    b = b-m;
	ans = b / 7;
	b %= 7;
	//////////////////////
    if(ans > m || (ans == m && b > 0)) ans = m - 1;
    else if(b == 3 && ans == m - 1) --ans;
    printf("%d\n",ans);
}
