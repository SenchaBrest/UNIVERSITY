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

	void add_first(string _valToAdd) {
        if (is_empty()) return;
		Node* p = new Node(_valToAdd);
		p->next = first;
		first = p;
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

int main() {
    list l;
    string dataLabel, data;
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
        cout << "\nEnter the value of the element before which you want to add the new element." << endl;
	    cin >> dataLabel;
	    cout << "Enter the value of the element you want to add." << endl;
	    cin >> data;	

	    int  i = 0;
	    if (l[0]->val == dataLabel)	{
	    	l.add_first(data);
	    	i = 2;
	    }
	    while (l[i] != nullptr) {
	    	if (l[i]->val == dataLabel) {
	    		Node* p = new Node(data);
	    		Node* buffer = new Node(dataLabel);
	    		buffer->next = l[i - 1]->next;
        		l[i - 1]->next = p;
	    		p->next = buffer->next;
        		delete buffer;
                i++;
	    	}
	    	i++;
	    }
        l.print();	
    }
}