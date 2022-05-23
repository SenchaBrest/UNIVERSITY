#include <iostream>
#include <random>
using namespace std;

void nMaxMin(double* &arr, int N) 
{    
    double max = arr[0], min = arr[0];
    int nMax = 0, nMin = 0;
    for (int i = 1; i < N; i++)
    {
        if (arr[i] > max)
        {
            max = arr[i];
            nMax = i;
        }
        if (arr[i] < min)
        {
            min = arr[i];
            nMin = i;
        }
    }
    cout << "nMin = " << nMin << ", nMax = " << nMax;
}
int main()
{
    setlocale(LC_CTYPE, "rus");
    int NA, NB, NC;
    cout << "Введите количество элементов массива A:";
    cin >> NA;
    cout << "Введите количество элементов массива B:";
    cin >> NB;
    cout << "Введите количество элементов массива C:";
    cin >> NC;

    double* A = new double[NA];
    double* B = new double[NB];
    double* C = new double[NC];

    random_device rand;
    mt19937 gen(rand());
    uniform_real_distribution<> dist(-100, 100);

    cout << "\n" << "A:" << "\t";
    for (int i = 0; i < NA; i++)
    {
        A[i] = dist(gen);
        cout << A[i] << "\t";
    }
    cout << "\n" << "B:" << "\t";
    for (int i = 0; i < NB; i++)
    {
        B[i] = dist(gen);
        cout << B[i] << "\t";
    }
    cout << "\n" << "C:" << "\t";
    for (int i = 0; i < NC; i++)
    {
        C[i] = dist(gen);
        cout << C[i] << "\t";
    }

    cout << "\nA:\t"; nMaxMin(A, NA);
    cout << "\nB:\t"; nMaxMin(B, NB);
    cout << "\nC:\t"; nMaxMin(C, NC);
    
    delete[] A;
    delete[] B;
    delete[] C;
}