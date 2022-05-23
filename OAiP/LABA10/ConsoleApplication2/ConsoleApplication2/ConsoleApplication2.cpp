#include <iostream>
#include <cstdlib>
#include <string>

void LowCaseRus(std::string &S) {
    for (int i = 0; i < S.size(); i++) {

        if (((int)S[i] >= -64) & ((int)S[i] < -32)) {
            S[i] = char(int(S[i]) + 32);
        }

        if ((int)S[i] == -88) {
            S[i] = char(int(S[i]) + 16);
        }
    }

}

int main() {

    system("chcp 1251>nul");

    std:: string one = "АаБбВвГгДдЕеЖжЗзИиКкЛлМмНнОоПпРрСсТтУуФфХхЦцЧчШшЩщЪъЫыЬьЭэЮюЯя";
    std::string two = "En:Aa Ru:Аа";
    std::string three = "Ёё";
    std::string four = "Язык";
    std::string five = "Lang";

    LowCaseRus(one);
    std::cout << one<<"\n";
    
    LowCaseRus(two);
    std::cout << two << "\n";

    LowCaseRus(three);
    std::cout << three << "\n";

    LowCaseRus(four);
    std::cout << four << "\n";

    LowCaseRus(five);
    std::cout << five << "\n";
    
}


