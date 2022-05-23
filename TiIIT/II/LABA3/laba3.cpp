#include <iostream>
#include <cstdlib>
#include <math.h>
using namespace std;
float y(float x, float b) {

    return cos(x) + \
        1 / b * cos(9 * x + 1) + \
        1 / pow(b, 2) * cos(pow(9, 2) * x + 2) + \
        1 / pow(b, 3) * cos(pow(9, 3) * x + 3) + \
        1 / pow(b, 4) * cos(pow(9, 4) * x + 4);
}
int randomRange(int min, int max)
{
    return int(double(rand()) / RAND_MAX * (max - min)) + min;
}
int main() {
    setlocale(LC_CTYPE, "rus");

    float x0, x1, alfa, b, alfaMin = 0.00000001, c = 0.8;
    cout << "Введите начальную точку х0: ";
    cin >> x0;

    cout << "Введите начальный шаг alfa: ";
    cin >> alfa;

    cout << "Введите значение b: ";
    cin >> b;

    int Nmax, n;
    cout << "Введите количество итераций Nmax: ";
    cin >> Nmax;

    cout << "Введите параметр терпения n: ";
    cin >> n;
    int j = n;
    float rand;
    for (int i = 0; i < Nmax; i++) {

        rand = (float)randomRange(-10000, 10000) / 10000;
        x1 = x0 + alfa * rand;

        if (y(x1, b) < y(x0, b)) {
            x0 = x1;
            j = n;
            cout << "\n" << x0 << " : " << y(x0, b);
        }
        else --j;
        alfa *= c;
        //if (alfa <= alfaMin) break;
        //if (j <= 0) break;
    }
    cout << "\n Ответ: " << x0 << " : " << y(x0, b);
}