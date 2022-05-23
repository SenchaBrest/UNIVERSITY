#include <iostream>
#include <string>
#include <stdlib.h>
using namespace std;

bool is_left;
int tabs = 0;
int MAX = 0;
int MIN = 100;
string s = "Way: ";

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
        if (_val < q->val) {
            if (q->left == nullptr) {
                Node* p = new Node(_val);
                q->left = p;
                return;
            }
            q = q->left;
        }
        else {
            if (q->right == nullptr) {
                Node* p = new Node(_val);
                q->right = p;
                return;
            }
            q = q->right;
        }
        push_back(_val, q);
    }  

    void search(int _val, Node* minor_root) {
        if (is_empty()) {
            cout << "Tree is empty.";
            return;
        }
        if (!minor_root) {
            cout << "This element doesn't exist.";
            return;
        }
        Node* q = minor_root;
        if (_val < q->val) {
            q = q->left;
            s += "Left. ";
        }
        else if (_val > q->val){
            q = q->right;
            s += "Right. ";
        }
        else {
            s += "There.";
            cout << s;
            return;
        }
        search(_val, q);
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

    void depth(Node* minor_root, int k) {
        if (!minor_root) {
            if (k < MIN) MIN = k - 1;
            return; 
        }        
        depth(minor_root->left, k + 1);

        if (k > MAX) MAX = k;

        depth(minor_root->right, k + 1);
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
    cout << "\n\n";
    cout << "Enter the values you need to search:" << endl;
    cin >> data;
    tr.search(atoi(data.c_str()), tr.root);
    cout << "\n\n";
    tr.depth(tr.root, 0);
    cout << "MAX: " << MAX << ".\tMIN: " << MIN << ".";
    tr.free_tree(tr.root);
}