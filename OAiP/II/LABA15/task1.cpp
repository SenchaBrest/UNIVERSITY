#include <iostream>
#include <string>
#include <stdlib.h>
using namespace std;

bool is_left;
int tabs = 0;

struct Node {
    int val;
    Node* left;
    Node* right;

    Node(int _val) : val(_val), left(nullptr), right(nullptr) {}
};

struct tree {
    Node* root;

    tree() : root(nullptr) {}

    bool is_empty() {
        return root == nullptr;
    }

    void push_back(int _val, Node* minor_root) {
        
        if (is_empty()) {
            Node* p = new Node(_val);
            root = p;
            return;
        }

        Node* q = minor_root;
        
        if (q->left == nullptr) {
            Node* p = new Node(_val);
            q->left = p;
            is_left = true;
            return;
        }
        if (q->right == nullptr) {
            Node* p = new Node(_val);
            q->right = p;
            is_left = false;
            return;
        }
        if (is_left) {
            push_back(_val, q->right);
        }
        else {
            push_back(_val, q->left);
        }
    }  

    void print(Node* minor_root) {
        if (!minor_root) return; 

        tabs++; 
        print(minor_root->left);

        for (int i = 0; i < tabs; i++) cout << " "; 
        cout << minor_root->val << endl; 

        print(minor_root->right);
        tabs--; 
        return;
    }

    void task1(Node* minor_root) {
        if (!minor_root) return; 

        
        task1(minor_root->left);

        if (minor_root->val < 0) {
            minor_root->val = abs(minor_root->val);
        }
        else {
            minor_root->val = 0;
        }
        
        task1(minor_root->right);
        return;
    }
    
    void free_tree(Node* minor_root) {
	    if (!minor_root) return;
	    free_tree(minor_root->left);
	    free_tree(minor_root->right);
	    delete minor_root;
	    return;
    }
};

int main() {
    tree tr;
    string data;
	cout << "Enter the values you need to write to the list. To stop recording write 'q':" << endl;
	while (1) {
		cin >> data;
		if (data == "q") {
			break;
		}

        try {
           tr.push_back(atoi(data.c_str()), tr.root);
        }
        catch(const std::exception& e) {
            std::cerr << e.what() << '\n';
        }
	}
    cout << "\n\n";
    tr.print(tr.root);
    tr.task1(tr.root);
    cout << "\n\n";
    tr.print(tr.root);
    tr.free_tree(tr.root);
}
