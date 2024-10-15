#include <stdio.h>
#include <string.h>

#define MSG_LEN 60

// Caesar cipher
void Caesar(char *message, int k) { // Receive the message and the shift number
    int idx = 0; // Declare idx to store the index of the message
    while(message[idx] != '\0') { // Use while loop to iterate the string, until the end of the string
        char *c = &message[idx];// Use pointer and idx to access the character of string
        if (*c >= 'A' && *c <= 'Z') { // If the character is uppercase
            *c = (*c - 'A' + k) % 26 + 'A'; // Use the formula to shift the character, and wrap around if the character is out of range
        }
        else if (*c >= 'a' && *c <= 'z') { // If the character is lowercase
            *c = (*c - 'a' + k) % 26 + 'a'; // Use the formula to shift the character, and wrap around if the character is out of range
        }
        idx++; // Increment idx
    }
}

// Reverse the string
void reverse(char *message) { // Receive the message
    int temp;
    char *p = message + strlen(message)-1;// Declare a temp variable and a pointer to the end of the string
    while (p > message) { // Use while loop to iterate the string, until the pointer is at the beginning of the string
        // Swap the character at the beginning and the end of the string
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
    int n; // Declare n to store the number of test cases
    scanf("%d", &n); // Read the input of test cases
    getchar(); // Use getchar() to read the newline character, otherwise the newline character will be read in the next read_line()
    while (n > 0) { // Use while loop to iterate the test cases
        char msg[MSG_LEN]; // Declare msg to store the message, +1 for the null character
        int k; // Caeser cipher shift number
        read_line(msg, MSG_LEN-1); // Read the message
        scanf("%d", &k); // Read the shift number
        getchar(); // Use getchar() to read the newline character
        Caesar(msg, k);// Call the Caesar function
        reverse(msg);// Call the reverse function
        printf("%s\n", msg);// Print the message
        n--;
    }
    return 0;
}