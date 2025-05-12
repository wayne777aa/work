#include<bits/stdc++.h>
using namespace std;

struct Node{
	int data;
	Node *left, *right;
};

// Recursively construct subtree under given root using
// leftChild[] and rightchild
Node * buildCartesianTreeUtil (int root, int arr[], int parent[], int leftchild[], int rightchild[]){
	if (root == -1)
		return NULL;

	// Create a new node with root's data
	Node *temp = new Node;
	temp->data = arr[root];

	// Recursively construct left and right subtrees
	temp->left = buildCartesianTreeUtil( leftchild[root], arr, parent, leftchild, rightchild );
	temp->right = buildCartesianTreeUtil( rightchild[root],	arr, parent, leftchild, rightchild );

	return temp;
}

// A function to create the Cartesian Tree in O(N) time
Node * buildCartesianTree (int arr[], int n){
	// Arrays to hold the index of parent, left-child,
	// right-child of each number in the input array
	int parent[n],leftchild[n],rightchild[n];

	// Initialize all array values as -1
	memset(parent, -1, sizeof(parent));
	memset(leftchild, -1, sizeof(leftchild));
	memset(rightchild, -1, sizeof(rightchild));

	// 'root' and 'last' stores the index of the root and the
	// last processed of the Cartesian Tree.
	// Initially we take root of the Cartesian Tree as the
	// first element of the input array. This can change
	// according to the algorithm
	int root = 0, last;

	// Starting from the second element
	for (int i=1; i<=n-1; i++){
		last = i-1;
		rightchild[i] = -1;

		// Scan upward from the node's parent up to
		// the root of the tree until a node is found
		// whose value is less than the current one
		// This is the same as Step 2 mentioned in the
		// algorithm
		while (arr[last] >= arr[i] && last != root)
			last = parent[last];

		// arr[i] is the smallest element yet; make it
		// new root
		if (arr[last] >= arr[i]){
			parent[root] = i;
			leftchild[i] = root;
			root = i;
		}else if (rightchild[last] == -1){
			rightchild[last] = i;
			parent[i] = last;
			leftchild[i] = -1;
		}else{
			parent[rightchild[last]] = i; // last的右子樹放到i左邊
			leftchild[i] = rightchild[last];
			rightchild[last] = i;
			parent[i] = last;
		}

	}

	// Since the root of the Cartesian Tree has no
	// parent, so we assign it -1
	parent[root] = -1;

	return (buildCartesianTreeUtil (root, arr, parent,
									leftchild, rightchild));
}

void binaryEncode(Node* node, vector<int>& bits) {
    if (!node) return;

    // 左子樹有 or 無
    bits.push_back(node->left ? 1 : 0);
    binaryEncode(node->left, bits);
    // 右子樹有 or 無
    bits.push_back(node->right ? 1 : 0);
    binaryEncode(node->right, bits);
    
}

int encodeToInt(const vector<int>& bits) {
    int code = 0;
    for (int b : bits) {
        code = (code << 1) | b;
    }
    return code;
}

// Pre-order 序列化，遇到 null 記錄 -1
void serialize(Node* node, vector<int>& result) {
	if (!node) {
		result.push_back(-1);
		return;
	}
	result.push_back(node->data);
	serialize(node->left, result);
	serialize(node->right, result);
}

// 把序列 hash 成整數
int encode(const vector<int>& seq) {
	int code = 0;
	const int MOD = 1e9 + 7;
	const int BASE = 13331;
	for (int x : seq) {
		code = (1LL * code * BASE + (x + 1000000)) % MOD;  // 防負數
	}
	return code;
}

int main(){
    int k,m;
    cin >> k >> m;

    for(int i=0;i<m;i++){
        int arr[k];
        for(int j=0;j<k;j++){
            cin >> arr[j];
        }

        Node *root = buildCartesianTree(arr, k);

        vector<int> bits;
		binaryEncode(root, bits);

		int code = encodeToInt(bits);

        cout << code << '\n';
    }

	return 0;
}
