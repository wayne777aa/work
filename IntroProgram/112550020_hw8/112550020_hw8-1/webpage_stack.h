#ifndef WEBPAGE_STACK_H
#define WEBPAGE_STACK_H

#include <stdbool.h>
#include "webpage.h"

// WebPageStack is a stack of WebPage pointers
// The stack is implemented as a dynamic array
// The pointer to the array is stored in _contents
// Each position in the array stores a pointer to a WebPage

typedef struct webpage_stack {
    WebPage **_contents;
    int _top, _capacity;
} WebPageStack;

void make_empty(WebPageStack *s, int size);
bool is_empty(const WebPageStack *s);
int size(const WebPageStack *s);
void push(WebPageStack *s, WebPage *i);
void pop(WebPageStack *s);
WebPage *peek(const WebPageStack *s);
void clear_stack(WebPageStack *s);

#endif