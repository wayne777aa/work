# include <stdio.h>
# include <stdlib.h>

typedef struct node{
    int data;
    struct node* next;
} Node;

Node *head = NULL;

void insert(int p, int d){

    Node *node = head;
    Node *new = malloc(sizeof(struct node));
    new->data = d;
    if(p == 0){
        new->next = head;
        head = new;
    }else{
    for(int i=0 ; i<p-1 || node == NULL ;i++){   //N=1時不會跑才加或
        if(node == NULL){
            printf("Invalid insertion\n");
            return;
        }
        node = node->next;
    }
    new->next = node->next;
    node->next = new;
    }
}

void printList(){
    Node *node = head;
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
                printList();
                break;
            case 'C':
                freeList();
                break;
            default:
                printf("Wrong OP\n");
                break;
        }
    }
    return 0;
}
