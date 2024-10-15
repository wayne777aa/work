#include <stdio.h>
#include "custom_assert.h"

void custom_assert(const char *msg, char *file, int line){
    char buffer[100];
    sprintf (buffer,"assertion failed: %s:%d: %s\n", file, line, msg);
    printf("%s", buffer);
}