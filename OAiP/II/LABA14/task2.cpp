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
    string PATH_words = "file2_words.txt";
    string PATH_numbers = "file2_numbers.txt";
    string PATH_stack = "file2_stack.txt";
    ofstream file1_out;
    ofstream file2_out;
    ofstream file_stack_out;
    ifstream file1_in;
    ifstream file2_in;

    file1_out.open(PATH_words, ios_base::out);
    file1_out << "One\nTwo\nThree\nFour\nFive\nSix\nSeven\nEight\nNine\nTen";
    file1_out.close();
    file2_out.open(PATH_numbers, ios_base::out);
    file2_out << "1\n2\n3\n4\n5\n6\n7\n8\n9\n10";
    file2_out.close();

    file1_in.open(PATH_words, ios_base::in);
    file2_in.open(PATH_numbers, ios_base::in);
    string s1;
    string s2;
    while (getline(file1_in, s1) && getline(file2_in, s2)) { 
        st.add(s1);
        st.add(s2);
    }
    file1_in.close();
    file2_in.close();

    file_stack_out.open(PATH_stack, ios_base::out);
    Node* p = st.first;
    while (p) {
        file_stack_out << p->val << "\n";
        p = p->next;
    }
}