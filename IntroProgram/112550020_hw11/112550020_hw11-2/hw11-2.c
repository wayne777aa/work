# include <stdio.h>
# include <stdlib.h>

// You must not add or delete any line in this file.

typedef struct node{
    int data;
    struct node* next;
} Node;

Node *head = NULL;
int entries=0;

Node *last_pre = NULL, *last_cur = NULL; 
int cur_index=0; 

void delete(int p){
    Node *cur;
    if (p == 0) cur = head;
    else cur = last_cur; //else cur = last_pre;

    if (p >= entries)
        printf("Invalid deletion\n");
    else if (p == 0) {
        head = head->next;
        free(cur);
        entries--;
    }
    else{
        int count = p-cur_index;
        Node *pre = last_pre, *next = cur->next;
        while (count > 0) { //while (count >= 0) { 
            pre = cur;
            cur = next;
            next = next->next;
            count--;
        }
        pre->next = next;
        free(cur);
        last_pre = pre;
        last_cur = next; //last_cur = next;
        cur_index = p;
        if (last_cur == NULL) { 
            last_cur = next; 
            // cur_index--;
        }
        entries--;
    }
}

void insert(int p, int d){
    Node* node;
    if (p == 0) node = head; 
    else if (p == cur_index) node = last_pre; 
    else node = last_cur; 
    if (p > entries) 
        printf("Invalid insertion\n");
    else{
        int count = p; 
        count = count-cur_index-1;
        while(count > 0) {
            node = node->next;
            count--;
        }
        Node *newnode = malloc(sizeof(Node));
        newnode->data = d;
        if(p == 0) {
            newnode->next = node;
            head = newnode;
        }
        else{
            newnode->next = node->next;
            node->next = newnode;
        }
        last_pre = node;
        last_cur = newnode;
        cur_index = p;
        entries++;        
    }
}

void printList(){
    Node* node = head;
    while(node != NULL){
        printf("%d ", node->data);
        node = node->next;
    }
    printf("\n");
}

void freeList(){
    Node *cur = head, *tmp;
    while(cur != NULL){
        tmp = cur;
        cur = cur->next;
        free(tmp);
    }
    head = NULL;
    entries = 0;
}

int main(){
    int position, data;
    char op;
    while(scanf(" %c", &op) != EOF){
        switch(op){
            case 'A':
                scanf("%d%d", &position, &data);
                insert(position, data);
                break;
            case 'B':
                scanf("%d", &position);
                delete(position);
                break;
            default:
                printf("Wrong OP\n");
                break;
        }
    }
    printList();
    freeList();
    return 0;
}