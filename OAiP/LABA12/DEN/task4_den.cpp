#include <iostream>
#include <fstream>

using namespace std;

int main() {
    string PATH = "file4_den.txt";
    ifstream filei;
    filei.open(PATH, ios_base::in);

    filei.seekg(0, ios_base::end);
    int k = filei.tellg();
    int space = 0, sum_red_line = 0;
    for(int i = 0; i < k; i++) {
        filei.seekg(i, ios_base::beg); 
        char buffer[] = ""; 
        filei.read(buffer, 1);
        if (space == 5) {
            sum_red_line += 1;
            space = 0;
        }
        if (buffer[0] == ' ') space += 1;
    }
    cout << "The count of red lines: " << sum_red_line;
    filei.close();
}