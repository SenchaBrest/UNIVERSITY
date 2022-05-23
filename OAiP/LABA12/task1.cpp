#include <iostream>
#include <string>
#include <fstream>
#include <cstdlib>
#include <vector>
#include <cmath>
#include <windows.h>

using namespace std;

void task1();
void task2();
void task3();
void task4();
void task5();


int menu();
void(*masf[])() = {task1, task2, task3, task4, task5};

int main() {
	while(1) (*masf[menu()])();
}

int menu() {
	char n;
	do
	{	
		cout << "\t   Menu\n";
		cout << "\t1. Task 1.\n";
		cout << "\t2. Task 2.\n";
		cout << "\t3. Task 3.\n";
		cout << "\t4. Task 4.\n";
		cout << "\t5. Task 5.\n";
		cout << "\t6. Exit.\n";
		printf ("Make a choice: ");
		n = getchar();
        system("cls");
	}
	while(strchr("123456", n) == NULL);
	if(n == '6') exit(0);
	return n - 49;
}

void task1() {
	system("cls");
	cout << "\nYou are already in the first task.\n";
    system("pause");
}

void task2()
{
	system("cls");
	string PATH = "file2.txt";
    ofstream file_out;
    ifstream file_in;
    
    file_out.open(PATH, ios_base::out);
    for (int i = 0; i < 10; i++) {
        file_out << int(rand()) << "\t";
    }
    file_out.close();
    
    file_in.open(PATH, ios_base::in);
    string s, sum_s = "";
    while (getline(file_in, s)) {
        sum_s += s;       
    } 
    file_in.close();

    vector<int> arr;
    string split("\t");
    size_t prev = 0;
    size_t next;
    size_t delta = split.length();
    while ((next = sum_s.find(split, prev)) != string::npos){
        arr.push_back(atoi(sum_s.substr(prev, next-prev).c_str()));
        prev = next + delta;
    }  
    arr.push_back(atoi(sum_s.substr(prev).c_str()));

    int temp; 
    for (int i = 0; i < arr.size() - 1; i++) {
        for (int j = 0; j < arr.size() - i - 1; j++) {
            if (arr[j] > arr[j + 1]) {
                temp = arr[j];
                arr[j] = arr[j + 1];
                arr[j + 1] = temp;
            }
        }
    }
    file_out.open(PATH, ios_base::app);
    file_out << endl << endl;
    for (int i = 1; i < arr.size(); i++) {
        file_out << arr[i] << "\t";
    }
    file_out.close();
    system("pause");
}

void task3() {
    system("cls");
	string PATH = "file3.txt";
    ofstream file_out;
    ifstream file_in;
    
    file_out.open(PATH, ios_base::out);
    file_out << "One\nTwo\nThree\nFour\nFive\nSix\nSeven\nEight\nNine\nTen";
    file_out.close();
    
    file_in.open(PATH, ios_base::in);
    string s, sum_s = "";
    int i = 0;
    while (getline(file_in, s)) {
        i++;
        sum_s += s;       
    } 
    file_in.seekg(10, ios_base::end);
    cout << "Number of lines: " << i << endl;
    cout << "Number of characters: " << sum_s.length();
    file_in.close();
    system("pause");
}
void task4() {
	system("cls");
	cout <<"Enter the line number to delete: "<< endl;
    int lineNumberToDelete;
    cin >> lineNumberToDelete;

    string PATH = "file4.txt";
    ofstream file_out;
    ifstream file_in;
    
    file_out.open(PATH, ios_base::out);
    file_out << "One\nTwo\nThree\nFour\nFive\nSix\nSeven\nEight\nNine\nTen";
    file_out.close();
    
    file_in.open(PATH, ios_base::in);
    string s, sum_s = "";
    int i = 0;
    while (getline(file_in, s)) { 
        i++;
        if (i == lineNumberToDelete) continue;
        sum_s += s + "\n";
    }
    file_in.close();

    file_out.open(PATH, ios_base::out);
    file_out << sum_s;
    file_out.close();
    system("pause");
}

void task5() {
	system("cls");
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
    system("pause");
}