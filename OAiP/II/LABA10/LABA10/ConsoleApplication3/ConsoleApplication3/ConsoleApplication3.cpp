#include <iostream>
using namespace std;

int powerN(int x, int n)
{
    if (x == 0) 
    {
        cout << "Ошибка! Вы ввели неподдерживаемое число (0)!";
        return 0;
    }
    if (n < 0) return 1 / powerN(x, -n);
    if (n == 0) return 1;
    else return x * powerN(x, n - 1);
}
int main()
{
    setlocale(LC_ALL, "rus");
    double X;
    int oneN, twoN, threeN, fourN, fiveN;
    cout << "Введите число для возведения в степень:";
    cin >> X;
    cout << "Введите 5 степеней для этого числа.\n";
    cin >> oneN;
    cin >> twoN;
    cin >> threeN;
    cin >> fourN;
    cin >> fiveN;
    
    cout << oneN <<".\t" << powerN(X, oneN) << "\n";
    cout << twoN <<".\t" << powerN(X, twoN) << "\n";
    cout << threeN <<".\t" << powerN(X, threeN) << "\n";
    cout << fourN <<".\t" << powerN(X, fourN) << "\n";
    cout << fiveN <<".\t" << powerN(X, fiveN) << "\n";
}