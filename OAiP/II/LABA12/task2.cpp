#include <iostream>
#include <fstream>
#include <string>
#include <cstdlib>
#include <vector>

using namespace std;

int main() {
    string PATH = "file2.txt";
    ofstream file_out;
    ifstream file_in;
    
    file_out.open(PATH, ios_base::out);
    for (int i = 0; i < 10; i++) {
        file_out << int(rand()) << "\t";
    }
    file_out.close();
    
    file_in.open(PATH, ios_base::in);
    string s, sum_s = "";
    while (getline(file_in, s)) {
        sum_s += s;       
    } 
    file_in.close();

    vector<int> arr;
    string split("\t");
    size_t prev = 0;
    size_t next;
    size_t delta = split.length();
    while ((next = sum_s.find(split, prev)) != string::npos){
        arr.push_back(atoi(sum_s.substr(prev, next-prev).c_str()));
        prev = next + delta;
    }  
    arr.push_back(atoi(sum_s.substr(prev).c_str()));

    int temp; 
    for (int i = 0; i < arr.size() - 1; i++) {
        for (int j = 0; j < arr.size() - i - 1; j++) {
            if (arr[j] > arr[j + 1]) {
                temp = arr[j];
                arr[j] = arr[j + 1];
                arr[j + 1] = temp;
            }
        }
    }
    
    file_out.open(PATH, ios_base::app);
    file_out << endl << endl;
    for (int i = 1; i < arr.size(); i++) {
        file_out << arr[i] << "\t";
    }
    file_out.close();
}