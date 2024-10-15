#include <stdlib.h>
#include <assert.h>
#include "webpage_stack.h"

void make_empty(WebPageStack *s, int capacity) {
    s->_contents = (WebPage **)malloc(capacity * sizeof(WebPage *));
    s->_top = 0;
}

bool is_empty(const WebPageStack *s) {
    return s->_top == 0;
}

int size(const WebPageStack *s) {
    return s->_top;
}

void push(WebPageStack *s, WebPage *i) {
    if(s->_top == s->_capacity) {
        assert("Stack overflow. ");
    }

    s->_contents[s->_top++] = i;
}

void pop(WebPageStack *s) {
    if(is_empty(s)) {
        assert("Stack underflow. ");
    }

    --s->_top;
}

WebPage *peek(const WebPageStack *s) {
    if(is_empty(s)) {
        assert("The stack is empty. ");
        return 0;
    }
    return s->_contents[s->_top - 1];
}

void clear_stack(WebPageStack *s) {
    s->_top = 0;
}