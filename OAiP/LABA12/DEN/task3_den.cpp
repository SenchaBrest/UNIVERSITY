#include <iostream>
#include <fstream>
#include <string>

using namespace std;

int main() {
    string PATH = "file3_den.txt";
    ofstream file_out;
    
    int N;
    while (true) {
        cout << "Enter N: ";
        cin >> N;
        if (N > 0 && N < 27) break;
    }

    string s = "ABCDEFGHIJKLMNOPQRSTUVWXYZ";
    file_out.open(PATH, ios_base::out);
    for (int i = 1; i <= N; i++) {
        for (int j = 0; j < i; j++) {
            file_out << s[j];
        }
        for (int j = 1; j <= N - i; j++) {
            file_out << "*";
        }
        file_out << endl;
    }
    file_out.close();
}