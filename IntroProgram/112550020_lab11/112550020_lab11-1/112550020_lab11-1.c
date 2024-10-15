#include <stdio.h>
#include <stdlib.h>

typedef struct node{
    int value;
    struct node* next;
}Node;

Node* head = NULL;

void swap(int a, int b){
    Node* node1,* node2,* temp1,* temp2;
    node1 = malloc(sizeof(Node));
    temp1 = node1;
    node1->next = head;
    
    
    while(node1->next->value != a &&node1->next->value != b){
        node1 = node1->next;
    }
    node2 = node1->next;
    while(node2->next->value != a &&node2->next->value != b){
        node2 = node2->next;
    }

    if(node1->next == node2){
        temp2 = node2->next;
        if(node1->next == head)
            head = temp2;
        node2->next = node2->next->next;
        temp2->next = node2;
        node1->next = temp2;
        
    }else{
        temp1 = node1->next->next;
        temp2 = node2->next;
        if(node1->next == head)
            head = temp2;
        node2->next = node1->next;
        node1->next->next = temp2->next;
        node1->next = temp2;
        temp2->next = temp1;
    }
}

int main(){
    int n;
    head = malloc(sizeof(Node));
    Node* node = head;
    scanf("%d", &n);
    scanf("%d", &(node->value));
    for(int i=1; i<n; i++){
    Node* new;
    new = malloc(sizeof(Node));
    scanf("%d", &(new->value));
    node->next = new;
    node = node->next;
    }
    int a, b;
    while(scanf("%d %d", &a, &b) != EOF){
        swap(a,b);
    }

    node = head;
    for(int i=0; i<n; i++){
        printf("%d ", node->value);
        node = node->next;
    }
}