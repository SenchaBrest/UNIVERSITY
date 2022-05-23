#include <iostream>
#include <fstream>
#include <string>

using namespace std;

int main() {
    string PATH = "file3.txt";
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
        sum_s += s;       
    } 
    file_in.seekg(10, ios_base::end);
    cout << "Number of lines: " << i << endl;
    cout << "Number of characters: " << sum_s.length();
    file_in.close();
}