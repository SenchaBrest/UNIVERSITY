#include <iostream>
#include <fstream>
#include <string>
#include <cstdlib>
#include <vector>
#include <ctime>

using namespace std;

int main() {
    string PATH = "file2_den.txt";
    ofstream file_out;
    ifstream file_in;
    
    srand(time(NULL));
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

    int buff = 0; // для хранения перемещаемого значения
    int i, j; // для циклов 
    for (i = 1; i < arr.size(); i++) {
        buff = arr[i]; // запомним обрабатываемый элемент
        // и начнем перемещение элементов слева от него
        // пока запомненный не окажется меньше чем перемещаемый
        for (j = i - 1; j >= 0 && arr[j] > buff; j--) arr[j + 1] = arr[j]; 

        arr[j + 1] = buff; // и поставим запомненный на его новое место 
    }

    file_out.open(PATH, ios_base::app);
    file_out << endl << endl;
    for (int i = 1; i < arr.size(); i++) {
        file_out << arr[i] << "\t";
    }
    file_out.close();
}