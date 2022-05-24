#include <iostream>
#include <string>
#include <fstream>
#include <cstdlib>
#include <vector>
#include <cmath>
#include <windows.h>
#include <ctime>

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
	string PATH = "file2_den.txt";
    ofstream file_out;
    ifstream file_in;
    
    srand(time(NULL));
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

    int buff = 0; // для хранения перемещаемого значения
    int i, j; // для циклов 
    for (i = 1; i < arr.size(); i++) {
        buff = arr[i]; // запомним обрабатываемый элемент
        // и начнем перемещение элементов слева от него
        // пока запомненный не окажется меньше чем перемещаемый
        for (j = i - 1; j >= 0 && arr[j] > buff; j--) arr[j + 1] = arr[j]; 

        arr[j + 1] = buff; // и поставим запомненный на его новое место 
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
    system("pause");
}
void task4() {
	system("cls");
	string PATH = "file4_den.txt";
    ifstream filei;
    filei.open(PATH, ios_base::in);

    filei.seekg(0,ios_base::end);
    int k = filei.tellg();
    int space = 0, sum_red_line = 0;
    for(int i = 0; i < k; i++) {
        filei.seekg(i,ios_base::beg); 
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
    system("pause");
}

void task5() {
	system("cls");
	string PATH = "file5_den.txt";
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

        fileo.width(10); 
        fileo.precision(4);
        fileo << right << X;
        fileo.width(15); 
        fileo.precision(8);
        fileo << right << sin(X);

        fileo<<endl;
    }
    fileo.close();
    system("pause");
}