#include <iostream>
#include <fstream>
#include <cmath>

using namespace std;

int main() {
    string PATH = "file5.txt";
    ofstream fileo;
    fileo.open(PATH, ios_base::out);

    float A, B;
    int N;
    cout << "Enter A: ";
    cin >> A;
    cout << "Enter B: ";
    cin >> B;
    cout << "Enter N: ";
    cin >> N;

    float X = 0;
    for(int i = 0; i < N; i++) {
        X += (B - A) / N;

        fileo.width(8); 
        fileo.precision(4);
        fileo << right << X;
        fileo.width(12); 
        fileo.precision(8);
        fileo << right << sin(X);
        fileo.width(12); 
        fileo.precision(8);
        fileo << right << cos(X);

        fileo<<endl;
    }
    fileo.close();
}