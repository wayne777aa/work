#ifndef CUSTOM_ASSERT_H
#define CUSTOM_ASSERT_H

#define assert(EX) custom_assert(EX, __FILE__, __LINE__)

void custom_assert(const char *, char *, int);

#endif