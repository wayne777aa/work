#include<stdio.h>

int main()
{
    int x,y,z;
    int vx,vy,vz;

    scanf("(%d,%d,%d) (%d,%d,%d)", &x, &y, &z, &vx, &vy, &vz);
    printf("(%d,%d,%d)\n",x+vx, y+vy, z+vz);

    return 0;
}
