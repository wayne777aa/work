#include <stdio.h>
#include <string.h>
#include "webpage.h"
#include "browser.h"

int main() {
    char op[10];
    Browser b;
    init_browser(&b, 1000);

    while(scanf("%s", op) != EOF) {
        if (strcmp(op, "new") == 0) {
            char url[100], title[100];
            scanf("%s %s", url, title);
            navigate_to(&b, create_webpage(url, title));
        } else if (strcmp(op, "back") == 0) {
            navigate_back(&b);
        } else if (strcmp(op, "forward") == 0) {
            navigate_forward(&b);
        } else if (strcmp(op, "current") == 0) {
            puts("---");
            print_current_webpage(&b);
            puts("---");
        } else {
            printf("Invalid operation\n");
        }
    }
}