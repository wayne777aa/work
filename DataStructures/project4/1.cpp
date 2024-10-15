#include <iostream>
#include <cstdlib>
#include <string>
using namespace std;

struct Node
{
	Node* left;
	Node* right;
	char data;
};

struct Position{
    char c;
    int p;
};

Node* root = 0;

void Postorder(Node *current){
    if (current) {                      // if current != NULL
        Postorder(current->left);       // L
        Postorder(current->right);      // R
        cout << current->data ;         // V
    }
}



int main(){
    root = (Node *)malloc(sizeof(Node));
    string preord, inord;
    cin >> preord >> inord;
    Position position[preord.length()];
    root->data = preord[0];
    for(int i=0; i<preord.length();i++){//依preord往下，排在inord的位置
        position[i].c = preord[i];
        position[i].p = inord.find(position[i].c);
    }

    for(int i=1;i<preord.length();i++){
        Node* newnode = (Node *)malloc(sizeof(Node));
        newnode->data = position[i].c;
        Node* current = root;
        int left=-1,right=preord.length();
        for(int j=0;j<i;j++){
            if(position[j].p<left || position[j].p>right){ //縮小範圍
                continue;
            }
            if(position[i].p < position[j].p){
                if(current->left == nullptr){
                    current->left = newnode;
                    break;
                }
                current = current->left;
                right = position[j].p;
            }else if(position[i].p > position[j].p){
                if(current->right == nullptr){
                    current->right = newnode;
                    break;
                }
                current = current->right;
                left = position[j].p;
            }
        }
    }
    Postorder(root);
    cout << endl;
    return 0;
}