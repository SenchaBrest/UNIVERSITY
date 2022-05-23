#include <iostream>
#include <string>

using namespace std;

struct Node {
    string val;
    Node* next;

    Node(string _val) : val(_val), next(nullptr) {}
};

struct list {
    Node* first;
    Node* last;

    list() : first(nullptr), last(nullptr) {}

    bool is_empty() {
        return first == nullptr;
    }

    void push_back(string _val) {
        Node* p = new Node(_val);
        if (is_empty()) {
            first = p;
            last = p;
            return;
        }
        last->next = p;
        last = p;
    }

    void print() {
        if (is_empty()) return;
        Node* p = first;
        cout << "List: ";
        while (p) {
            cout << p->val << " ";
            p = p->next;
        }
        cout << endl;
    }

    Node* operator[] (const int index) {
        if (is_empty()) return nullptr;
        Node* p = first;
        for (int i = 0; i < index; i++) {
            p = p->next;
            if (!p) return nullptr;
        }
        return p;
    }

    ~list() {
        while (first != NULL) {
            Node *temp = first->next;   
            delete first;                
            first = temp;                  
        }
    }  
};

void task3(list l) {
	int i = 0, k = 0;
	while (l[i] != nullptr) {
		if ((l[i]->val)[0] == (l[i]->val)[(l[i]->val).length() - 1]) {
			k++;
		}
		i++;        
	}
	cout << "The number of words in the list that begin with the same letter as they end: " << k << endl; 
}

int main() {
    list l;
    string data;
	cout << "Enter the values you need to write to the list. To stop recording write 'q':" << endl;
	while (1) {
		cin >> data;
		if (data == "q") {
			break;
		}
		l.push_back(data);
	}
    l.print();
    if (l.is_empty()) {
		cout << "The list is empty." << endl;
	}
    else {
        task3(l);
    }
}