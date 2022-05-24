#include <iostream>
#include <cstdlib>
#include <string>
using namespace std;

void LowCaseRus(std::string& S) {
    for (int i = 0; i < S.size(); i++) 
    {
        if (((int)S[i] >= -32) & ((int)S[i] < 0)) 
        {
            S[i] = char(int(S[i]) - 32);
        }
        if ((int)S[i] == -72) 
        {
            S[i] = char(int(S[i]) - 16);
        }
    }
}

int main() 
{
    system("chcp 1251>nul");

    std::string one, two, three, four, five;
    cout << "Введите 5 произвольных строк\n";
    cin >> one >> two >> three >> four >> five;

    LowCaseRus(one); cout << one << "\n";
    LowCaseRus(two); cout << two << "\n";
    LowCaseRus(three); cout << three << "\n";
    LowCaseRus(four); cout << four << "\n";
    LowCaseRus(five); cout << five << "\n";
}