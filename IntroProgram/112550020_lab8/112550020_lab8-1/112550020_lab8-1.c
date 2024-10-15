#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <stdbool.h>

typedef struct stack {
    int *_contents;
    int _top, _capacity;
} Stack;

void make_empty(Stack *s, int size);
bool is_empty(const Stack *s);
int size(const Stack *s);

void push(Stack *s, int i){
    if(s->_top < s->_capacity){
    *(s->_contents+s->_top) = i;
    s->_top++;
    }else
    printf("Stack overflow. \n");
}

void pop(Stack *s){
    if(s->_top > 0){
    s->_top--;
    }else
    printf("Stack underflow. \n");
}
int peek(const Stack *s){
    if(s->_top > 0){
    return *(s->_contents+s->_top-1);
    }else
    printf("The stack is empty. \n");
    return 0;
}
void clear_stack(Stack *s);
void print_stack(const Stack *s);

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

void make_empty(Stack *s, int capacity) {
    s->_contents = (int *)malloc(capacity * sizeof(int));
    s->_top = 0;
    s->_capacity = capacity;
}

void clear_stack(Stack *s) {
    s->_top = 0;
    free(s->_contents);
}

bool is_empty(const Stack *s) {
    return s->_top == 0;
}

int size(const Stack *s) {
    return s->_top;
}

void print_stack(const Stack *s) {
    printf("Current stack contains: ");
    for (int i = s->_top - 1; i >= 0; i--) {
        printf("%d ", s->_contents[i]);
    }
    puts("");
}