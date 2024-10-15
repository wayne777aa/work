#include <stdio.h>
#include <stdlib.h>

typedef struct {
    int id;
    char *name;
} Student;

Student* createStudent(int id, const char *name) {
    Student *newStudent = (Student*)malloc(sizeof(Student));
    if (newStudent == NULL) {
        return NULL; // Memory allocation error
    }

    newStudent->id = id;
    newStudent->name = (char*)malloc(100 * sizeof(char));
    if (newStudent->name == NULL) {
        return NULL;
    }
    snprintf(newStudent->name, 100, "%s", name);
    return newStudent;
}

void processStudents(int count) {
    for (int i = 0; i < count; i++) {
        Student *s = createStudent(i, "StudentName");
        // Some processing with the student 's'
        printf("Processing student %d: %s\n", s->id, s->name);
        // free(s->name);
        // free(s);
    }
}

int main() {
    processStudents(5);
    printf("Students processed\n");
    return 0;
}