#include <iostream>
#include <fstream>
#include <string>

using namespace std;

int main() {
    cout <<"Enter the line number to delete: "<< endl;
    int lineNumberToDelete;
    cin >> lineNumberToDelete;

    string PATH = "file4.txt";
    ofstream file_out;
    ifstream file_in;
    
    file_out.open(PATH, ios_base::out);
    file_out << "One\nTwo\nThree\nFour\nFive\nSix\nSeven\nEight\nNine\nTen";
    file_out.close();
    
    file_in.open(PATH, ios_base::in);
    string s, sum_s = "";
    int i = 0;
    while (getline(file_in, s)) { 
        i++;
        if (i == lineNumberToDelete) continue;
        sum_s += s + "\n";
    }
    file_in.close();

    file_out.open(PATH, ios_base::out);
    file_out << sum_s;
    file_out.close();
}