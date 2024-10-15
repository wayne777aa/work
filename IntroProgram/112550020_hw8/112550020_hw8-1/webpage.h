#ifndef WEBPAGE_H
#define WEBPAGE_H

#define URL_MAX_LENGTH 2048
#define TITLE_MAX_LENGTH 256

typedef struct web_page {
    char url[URL_MAX_LENGTH];
    char title[TITLE_MAX_LENGTH];
} WebPage;

WebPage* create_webpage(char* url, char* title);
void destroy_webpage(WebPage* page);
void print_webpage(WebPage* page);
void deep_copy_webpage(WebPage* dest, WebPage* src);

#endif