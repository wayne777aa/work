#include <stdio.h>
#include <stdlib.h>
#include "webpage.h"
#include "webpage_stack.h"
#include "browser.h"

void init_browser(Browser* browser, int capacity) {
    make_empty(&browser->_back, capacity);
    make_empty(&browser->_forward, capacity);
    browser->_current = NULL;
}

void destroy_browser(Browser* browser) {
    clear_stack(&browser->_back);
    clear_stack(&browser->_forward);
    free(browser);
}

void print_current_webpage(Browser* browser) {
    if(browser->_current == NULL){
        printf("Empty\n");
        return;
    }
    print_webpage(browser->_current);
}

void navigate_to(Browser* browser, WebPage* page) {
    // printf("%d", (&browser->_back)->_top);
    (&browser->_back)->_contents[(&browser->_back)->_top++] = browser->_current;
    browser->_current = page;
    clear_stack(&browser->_forward);
}

void navigate_back(Browser* browser) {
    if((&browser->_back)->_top == 0 ||(&browser->_back)->_contents[(&browser->_back)->_top-1] == NULL){
        printf("Cannot navigate back\n");
        return;
    }
    (&browser->_forward)->_contents[(&browser->_forward)->_top++] = browser->_current;
    browser->_current = (&browser->_back)->_contents[(&browser->_back)->_top---1];
    // free((&browser->_back)->_contents[(&browser->_back)->_top-1]);

}

void navigate_forward(Browser* browser) {
    if((&browser->_forward)->_top == 0){
        printf("Cannot navigate forward\n");
        return;
    }
    (&browser->_back)->_contents[(&browser->_back)->_top++] = browser->_current;
    browser->_current = (&browser->_forward)->_contents[(&browser->_forward)->_top---1];

}