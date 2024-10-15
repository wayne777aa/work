#include <stdio.h>
#include <string.h>

#define MSG_LEN 60

// Caesar cipher
void Caesar(char *c, int k) { // Receive the message and the shift number
    while(*c != '\0') { // Use while loop to iterate the string, until the end of the string
        
        if (*c <= 'Z' && *c >= 'A') { // If the character is uppercase
            *c = (*c - 'A' + k) % 26 + 'A'; // Use the formula to shift the character, and wrap around if the character is out of range
        } 
        else if (*c <= 'z' && *c >= 'a') { // If the character is lowercase
            *c = (*c - 'a' + k) % 26 + 'a'; // Use the formula to shift the character, and wrap around if the character is out of range
        }
        c++;
    }
}

// Reverse the string
void reverse(char *message, int len) {
    char temp = *message;
    char *p = message + len-1;
    for(int i=0; i<len/2; i++) { // Use while loop to iterate the string, until the pointer is at the beginning of the string
        temp = *message;
        *message++ = *p;
        *p-- = temp;
    }
}

int read_line(char str[], int n) {
    int ch, i = 0;
    while (1) { 
        ch = getchar();
        if (ch == '\n' || ch == EOF)
            break;
        if (i < n)
            str[i++] = ch;
    }
    str[i] = '\0';
    return i;
}

int main() {
    int n;                              // Declare n to store the number of test cases
    scanf("%d", &n);                    // Read the input of test cases
    getchar();                          // Use getchar() to read the newline character, otherwise the newline character will be read in the next read_line()
    while (n > 0) {                     // Use while loop to iterate the test cases
        char msg[MSG_LEN+1];            // Declare msg to store the message, +1 for the null character
        int k, len;                          // Caeser cipher shift number
        len = read_line(msg, MSG_LEN);        // Read the message
        scanf("%d", &k);                // Read the shift number
        getchar();                      // Use getchar() to read the newline character
        Caesar(msg, k);
        reverse(msg, len);
        printf("%s\n", msg);
        n--; 
    }
    return 0;
}