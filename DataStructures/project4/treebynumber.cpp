#include <iostream>
using namespace std;

struct Node
{
	// Node* parent;
	Node* left;
	Node* right;
	int data;
};

Node* root = 0;

void Postorder(Node *current){
    if (current) {                      // if current != NULL
        Postorder(current->left);       // L
        Postorder(current->right);      // R
        cout << current->data ;         // V
        if(current->data != root->data)
            cout << " ";
    }
}

int main(){
    root = (Node *)malloc(sizeof(Node));
    
    int n;
    cin >> n;
    int top;
    cin >> top;
    root->data = top;
    for(int i=1;i<n;i++){
        int val;
        cin >> val;
        Node* newnode = (Node *)malloc(sizeof(Node));
        newnode->data = val;
        Node* current = root;
        while(1){
            if(val < current->data){
                if(current->left == nullptr){
                    current->left = newnode;
                    // newnode->parent = current;
                    break;
                }
                current = current->left;
            }else{
                if(current->right == nullptr){
                    current->right = newnode;
                    // newnode->parent = current;
                    break;
                }
                current = current->right;
            }
        }
    }
    Postorder(root);
    cout << endl;
    return 0;
}