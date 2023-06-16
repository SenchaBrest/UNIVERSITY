#include <iostream>
#include <vector>
#include <sstream>
#include <string>
#include <algorithm>
#include <fstream>
using namespace std;
#define INF 9999999
void print_traveling_salesman(int arr[], vector<vector<int>> matrix, int start) {
        int size_path = 0;
        vector<int> size;//вектор содержащий стоимость от точки до точки
        cout << "path: ";
        for(int j = 0;j<matrix.size(); j++){
            if(j != matrix.size() - 1){
                size_path += matrix[ arr[j]-1 ][ arr[j+1]-1 ];
                size.push_back(matrix[ arr[j]-1 ][ arr[j+1]-1 ]);
            }
            else{//возвращение в стартовую точку
                size_path += matrix[ arr[j]-1 ][ arr[0] - 1];
                size.push_back(matrix[ arr[j]-1 ][ arr[0] - 1 ]);
            }cout << arr[j] <<" ";
        }
        cout<<start + 1;
        cout<<"   size_path: "<<size_path;
        cout<<"   price: ";
        for(auto elem: size){cout<<elem<<" "; } 
        cout<<endl;
    }
    void traveling_salesman(int arr[], int n, vector<vector<int>> matrix,int start,int k = 0) {//перестановки для комивояжёра
        int temp = arr[start];
        for (int i = start; i > 0; i--) { arr[i] = arr[i-1]; }
        arr[0] = temp;
        while (true) {//генерация перестановок
            if(arr[0] == start + 1){//если стартовая точка стоит в начале перестановок, то переставляем следующие 5 элементов
                print_traveling_salesman(arr, matrix,start);
                int i = n - 2;// Ищем индекс первого элемента, который можно заменить
                while (i >= 0 && arr[i] >= arr[i+1]) { i--; }
                // Если такого элемента нет, завершаем цикл
                if (i < 0) { break; }
                // Ищем индекс первого элемента справа от arr[i], который меньше arr[i]
                int j = n - 1;
                while (arr[i] >= arr[j]) { j--; }
                swap(arr[i], arr[j]);// Меняем местами arr[i] и arr[j]
                reverse(arr + i + 1, arr + n);// Переворачиваем массив справа от arr[i]
            } else break;// чтобы не делать лишние расчеты перестановок, когда стартовая точка не в начале
        }}
int main() {
    string filename = "task1.txt";
    vector<vector<int>> matrix;
    ifstream file(filename);
    if (file.is_open()) {
        string line;
        while (getline(file, line)) {
            vector<int> row;
            istringstream iss(line);
            string num;
            while (iss >> num) {
                if (num == "∞") { row.push_back(INF); } 
                else { row.push_back(stod(num)); }
            }matrix.push_back(row);
        }
        file.close();
        for (auto row : matrix) {
            for (auto num : row) { cout << num << " "; }
            cout << endl;
        }
    } else { cout << "Error opening file: " << filename << endl; }
    int start = 2;
    int num = matrix.size();
    int arr[num];
    for(int i = 1; i <=num;i++){ arr[i-1] = i; }
    traveling_salesman(arr,num,matrix,start);
    return 0;
}