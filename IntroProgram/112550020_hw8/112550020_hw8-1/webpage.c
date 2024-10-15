#include <stdio.h>
#include <string.h>
#include <stdlib.h>
#include "webpage.h"

WebPage* create_webpage(char* url, char* title) {
    WebPage* page = (WebPage*)malloc(sizeof(WebPage));
    strcpy(page->url, url);
    strcpy(page->title, title);
    return page;
}

void destroy_webpage(WebPage* page) {
    free(page->url);
    free(page->title-2048);
    free(page);
}

void print_webpage(WebPage* page) {
    printf("Title: %s\n", page->title);
    printf("URL: %s\n", page->url);
}

void deep_copy_webpage(WebPage* dest, WebPage* src) {
    strcpy(dest->url, src->url);
    strcpy(dest->title, src->title);
}