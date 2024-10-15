#include <stdio.h>
//直角三角形 正三角形 等腰三角形 !!!有可能有等腰直角三角形
int main()
{
    int side1, side2, side3;
    scanf("%d %d %d",&side1, &side2, &side3);
    if(side1 > side2){}
    if(side1*side1 + side2*side2 == side3*side3 || side1*side1 + side3*side3 == side2*side2 || side2*side2 + side3*side3 == side1*side1)
    {
        printf("Rectangle triangle\n");
    }
    else if(side1 == side2 && side2 == side3)
    {
        printf("Regular triangle\n");
    }
    else if(side1 == side2 || side2 == side3 || side1 == side3)
    {
        printf("Isosceles triangle\n");
    }
    return 0;
}