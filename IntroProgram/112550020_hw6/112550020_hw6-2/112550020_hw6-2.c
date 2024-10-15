# include <stdio.h>
# include <stdlib.h>

typedef struct node{
    int data;
    struct node* next;
} Node;

void printList();

Node *head = NULL;

void insert(int p, int d){

    static int a = 0;
    static Node *node;
    int copy = a;
    if(a == 0)
    node = head;
    Node *new = malloc(sizeof(struct node));
    new->data = d;
    if(p == 0){
        new->next = head;
        head = new;
    }else{
    Node *ncopy = node;
    for(int i=a ; i<p-1 || node == NULL ;i++){
        if(node == NULL){
            printf("Invalid insertion\n");
            a = copy;
            node = ncopy;
            return;
        }
        node = node->next;
        a++;
    }
    new->next = node->next;
    node->next = new;
    }
}

void delete(int p){
    static int D = 0;
    static int b = 0;
    int copy = b;
    static Node *node, *tem;
    
    if(b == 0|| D == 0){
    node = head;
    D++;
    }
    Node *ncopy = node;
    for(int i=b ; i<p-1 || node == NULL ;i++){
        if(node == NULL){
            printf("Invalid deletion\n");
            b = copy;
            node = ncopy;
            return;
        }
        node = node->next;
        b++;
    }
    if(p != 0){ 
        if(node->next == NULL){ //處理p是下一個 eg. 1 2有node p==3
            printf("Invalid deletion\n");
            b = copy;
            node = ncopy;
            return;
        }else{
            tem = node->next;
            node->next = (node->next)->next;
            free(tem);
        }
    }
    else{ 
        tem = head;
        head = head->next;
        free(tem);
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