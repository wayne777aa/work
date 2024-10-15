#include <stdio.h>
#include "ta_lib.h"
#define MAX_CALLBACKS 100

void example_add(_CUSTOM_PARAMS_T params) {
    printf("Meow answer is %d\n", params.arg1 + params.arg2);
}

void example_mul(_CUSTOM_PARAMS_T params) {
    printf("Meow answer is %d\n", params.arg1 * params.arg2);
}

void example_sub(_CUSTOM_PARAMS_T params) {
    printf("Meow answer is %d\n", params.arg1 - params.arg2);
}

void example_div(_CUSTOM_PARAMS_T params) {
    printf("Meow answer is %.2f\n", (float)params.arg1 / params.arg2);
}

typedef struct{
    char tag_name[100];
    void (*callback)(_CUSTOM_PARAMS_T params);
}   CallbackEntry;

CallbackEntry callbacks[MAX_CALLBACKS];
int callback_count = 0;

void student_register_callback(char tag_name[], void (*FPTR)(_CUSTOM_PARAMS_T params)) {
    // if CallbackEntry still has space
    if (callback_count < MAX_CALLBACKS) {
        // copy tag_name to CallbackEntry
        strcpy(callbacks[callback_count].tag_name, tag_name);
        // copy FPTR to CallbackEntry
        callbacks[callback_count].callback = FPTR;
        // What should you do else?
        ++callback_count;
    }
}

void student_run(char tag_name[], _CUSTOM_PARAMS_T params) {
    // Find the callback function by tag_name
    for (int i = 0; i<callback_count; i++) {
        if (strcmp(callbacks[i].tag_name, tag_name) == 0) {
            callbacks[i].callback(params); // Call the callback function
            break;
        }
    }
}

int main(int argc, char **argv) {
    _CUSTOM_PARAMS_T m_params;
    m_params.arg1 = 1; 
    m_params.arg2 = 2;

    student_register_callback("add", example_add);
    student_register_callback("mul", example_mul);
    student_register_callback("sub", example_sub);
    student_register_callback("div", example_div);
    
    // You can register more function by yourself, enjoy it
    // ta_register_callback("ohmygod", balabala_my_cb_func);

    printf("===== Student example =====\n");

    // Add example
    printf("Action 1: ");
    student_run("add", m_params);

    printf("Action 2: ");
    m_params.arg1 = 2;
    m_params.arg2 = 3;
    student_run("sub", m_params);

    // Mul example
    printf("Action 3: ");
    m_params.arg1 = 5;
    m_params.arg2 = 3;
    student_run("mul", m_params);

    printf("Action 4: ");
    m_params.arg1 = 2;
    m_params.arg2 = 3;
    student_run("div", m_params);

    

    return 0;
}
