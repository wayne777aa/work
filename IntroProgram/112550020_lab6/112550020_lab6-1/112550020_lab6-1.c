# include <stdio.h>
# define N 10000

void push(int element, int *head, int *tail){

    *tail = element;
}
void pop(int *head, int *tail){
    printf("%d ", *head);
}
void peak(int *head, int *tail){
    printf("%d ", *(tail-1));
}

int main(){
    int arr[N], element, *head=&arr[0], *tail=&arr[0];
    char op;
    while(scanf(" %c", &op) != EOF){
        switch(op){
            case 'A':
                scanf("%d", &element);
                push(element, head, tail);
                tail++;
                break;
            case 'B':
                pop(head, tail);
                head++;
                break;
            case 'C':
                peak(head, tail);
                break;
            default:
                printf("Wrong OP\n");
                break;
        }
    }
    return 0;
}