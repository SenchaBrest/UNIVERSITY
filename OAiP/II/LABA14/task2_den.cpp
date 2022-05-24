#include <iostream>
#include <string>
#include <fstream>

using namespace std;

struct Node {
    string val;
    Node* next;

    Node(string _val) : val(_val), next(nullptr) {}
};

struct stack {
    Node* first;

    stack() : first(nullptr) {}

    bool is_empty() {
        return first == nullptr;
    }

	void add(string _valToAdd) {
        Node* p = new Node(_valToAdd);
        if (is_empty()) {
            first = p;
            return;
        }
		p->next = first;
		first = p;
    }

    ~stack() {
        while (first != NULL) {
            Node *temp = first->next;   
            delete first;                
            first = temp;                  
        }
    }
};

int main() {
    stack st;
    string PATH_begin = "file2_begin.txt";
    string PATH_end = "file2_end.txt";
    ofstream file_begin_out;
    ofstream file_end_out;
    ifstream file_begin_in;

    file_begin_out.open(PATH_begin, ios_base::out);
    file_begin_out << "One\nTwo\nThree\nFour\nFive\nSix\nSeven\nEight\nNine\nTen";
    file_begin_out.close();

    file_begin_in.open(PATH_begin, ios_base::in);
    string s;
    while (getline(file_begin_in, s)) { 
        st.add(s);
    }
    file_begin_in.close();

    file_end_out.open(PATH_end, ios_base::out);
    Node* p = st.first;
    while (p) {
        file_end_out << p->val << "\n";
        p = p->next;
    }
}