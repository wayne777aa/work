#ifndef BROWSER_H
#define BROWSER_H

#include "webpage.h"
#include "webpage_stack.h"

typedef struct browser {
    WebPageStack _back;
    WebPageStack _forward;
    WebPage *_current;
    int _capacity;
} Browser;

void init_browser(Browser* browser, int capacity);
void destroy_browser(Browser* browser);
void print_current_webpage(Browser* browser);
void navigate_to(Browser* browser, WebPage* page);
void navigate_back(Browser* browser);
void navigate_forward(Browser* browser);

#endif
