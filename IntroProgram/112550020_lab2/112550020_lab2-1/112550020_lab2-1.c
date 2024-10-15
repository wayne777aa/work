#include<stdio.h>

int main()
{
    float height, weight, BMI;
    scanf("%f %f", &height, &weight);
    BMI = weight/(height/100)/(height/100);
    printf("BMI=%.2f, ",BMI);
    if(BMI<18.5){
        printf("Underweight\n");
    }   else
    if(BMI>=18.5&&BMI<24.9){
        printf("Normal weight\n");
    }   else
    if(BMI>=25.0&&BMI<29.9){
        printf("Overweight\n");
    }   else
    if(BMI>=30.0&&BMI<34.9){
        printf("Obese (class I)\n");
    }   else
    if(BMI>=35.0&&BMI<39.9){
        printf("Obese (class II)\n");
    }   else
        printf("Obese (class III)\n");

    return 0;
}