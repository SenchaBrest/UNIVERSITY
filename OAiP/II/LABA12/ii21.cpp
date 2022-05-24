#include <iostream>
#include <fstream>
#include <string>

using namespace std;

int main() {
    string PATH = "fio.txt";
    ofstream file_out;
    
    file_out.open(PATH, ios_base::out);
    file_out << "kirilovich arseniy first course ii21\n";
    file_out << "litvinuk timophey first course ii21\n";
    file_out.close();
}