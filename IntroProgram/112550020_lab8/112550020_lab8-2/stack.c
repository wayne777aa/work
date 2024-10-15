#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <stdbool.h>
#include "stack.h"
#include "custom_assert.h"

void push(Stack *s, int i){
#ifdef DEBUG
    print_stack(s);
    printf("pushing at stack\n");
#endif
    if(s->_top < s->_capacity){
    *(s->_contents+s->_top) = i;
    s->_top++;
    }else
    assert("Stack overflow.");
}

void pop(Stack *s){
#ifdef DEBUG
    print_stack(s);
    printf("popping at stack\n");
#endif
    if(s->_top > 0){
    s->_top--;
    }else
    assert("Stack underflow.");
}
int peek(const Stack *s){
#ifdef DEBUG
    print_stack(s);
    printf("Peeking at stack\n");
#endif
    if(s->_top > 0){
    return *(s->_contents+s->_top-1);
    }else
    assert("The stack is empty.");
    return 0;
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