#include <iostream>
#include <fstream>
#include <string>

using namespace std;

int main() {
    string PATH = "fio.txt";
    ofstream file_out;
    
    file_out.open(PATH, ios_base::app);
    file_out << "\ncorpach denis first course ii21\n";
    file_out.close();
}