#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <stdbool.h>
#include "stack.h"
#include "custom_assert.h"

int main() {
    char op[10];
    Stack s;
    make_empty(&s, 64);

    while(scanf("%s", op) != EOF) {
        if (strcmp(op, "push") == 0) {
            int i;
            scanf("%d", &i);
            push(&s, i);
        } else if (strcmp(op, "pop") == 0) {
            pop(&s);
        } else if (strcmp(op, "peek") == 0) {
            if(is_empty(&s))
                peek(&s);
            else 
                printf("%d\n", peek(&s));
        } else if (strcmp(op, "size") == 0) {
            printf("%d\n", size(&s));
        } else if (strcmp(op, "is_empty") == 0) {
            printf("%s\n", is_empty(&s) ? "The stack is empty. " : "The stack is not empty. ");
        } else if (strcmp(op, "clear") == 0) {
            print_stack(&s);    
            clear_stack(&s);
        } else {
            printf("Invalid operation\n");
        }
    }
}