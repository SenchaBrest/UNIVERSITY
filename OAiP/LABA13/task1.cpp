#include <iostream>
#include <windows.h>
#include <string>
#include <iomanip>
#include <fstream>
#include <vector>

using namespace std;

struct Date {
	int year = 0;
	int month = 0;
	int day = 0;
};

struct Address {
	int zipCode = 0;
	string country;
	string region;
	string district;
	string city;
	string street;
	int house = 0;
	int apartment = 0;
};

struct Patient {
	string surname;
	string name;
	string lastName;
	string sex;
	string nationality;
	float growth = 0;
	float weight = 0;
	struct Date dateOfBirth;

	string phoneNumber;
	struct Address homeAddress;

	int hospitalNumber = 0;
	string branch;
	int medicalCardNumber = 0;
	string diagnosis;
	string bloodType;
};

void create();
void viewing();
void add();
void remove();
void sort();

int menu();
void(*masf[])() = {create, viewing, add, remove, sort};

Patient* AddStruct();
void setData();
void recording();
void head();

int amount = 0;
int I = 0;
Patient* OurPatients = new Patient[0];
string PATH = "file1.txt";
ofstream file_out;
ifstream file_in;
int main() {
    head();
	while(1) (*masf[menu()])();

    try {
        delete[] OurPatients;
    }
    catch(const std::exception& e) {
        std::cerr << e.what() << '\n';
    }   
}

int menu() {
	char n;
	do {	
		cout << "\t   Menu\n";
		cout << "\t1. Create.\n";
		cout << "\t2. Viewing.\n";
		cout << "\t3. Add.\n";
		cout << "\t4. Delete.\n";
		cout << "\t5. Sort.\n";
		cout << "\t6. Exit.\n";
		printf ("Make a choice: ");
		n = getchar();
		system("cls");
	}
	while (strchr("123456", n) == NULL);
	if (n == '6') exit(0);
	return n - 49;
}

void create() {
	int YesOrNot = 0;
	do {
		OurPatients = AddStruct();
		setData();

		amount++;

		cout << "Continue entering data (1 - yes, 0 - no)?";
		cin >> YesOrNot;
		cin.get();
        recording();
        delete[] OurPatients;
        amount--;
	} while (YesOrNot != 0);
}

void viewing() {
    file_in.open(PATH, ios_base::in);
    string s, sum_s = "";
    while (getline(file_in, s)) { 
        sum_s += s + "\n";
    }
    file_in.close();

    cout << sum_s;
    system("pause");
}

void recording() {
    file_out.open(PATH, ios_base::app);
	for(int i = 1; i <= 300; i++) {
		file_out << "=";
	}
	file_out << endl;

	file_out << left << setw(3) << I + 1 << "|" << setw(15) << OurPatients[0].surname << "|" 
			<< setw(10) << OurPatients[0].name << "|" << setw(15) << OurPatients[0].lastName << "|"
	 		<< setw(6) << OurPatients[0].sex << "|" << setw(15) << OurPatients[0].nationality << "|" 
			<< setw(6) << OurPatients[0].growth << "|" << setw(6) << OurPatients[0].weight << "|"
			<< setw(2) << OurPatients[0].dateOfBirth.day << "." 
			<< setw(2) << OurPatients[0].dateOfBirth.month << "." << setw(4) << OurPatients[0].dateOfBirth.year
			<< "|" << setw(13) << OurPatients[0].phoneNumber << "|" << setw(15) << OurPatients[0].hospitalNumber << "|" 
			<< setw(6) << OurPatients[0].branch << "|" << setw(19) << OurPatients[0].medicalCardNumber << "|"
			<< setw(15) << OurPatients[0].diagnosis << "|" << setw(10) << OurPatients[0].bloodType << "|" 
            << setw(8) << OurPatients[0].homeAddress.zipCode << "|" << setw(10) << OurPatients[0].homeAddress.country << "|"
			<< setw(10) << OurPatients[0].homeAddress.region << "|" << setw(10) << OurPatients[0].homeAddress.district << "|"
			<< setw(10) << OurPatients[0].homeAddress.city << "|" << setw(20) << OurPatients[0].homeAddress.street << "|"
			<< setw(5) << OurPatients[0].homeAddress.house << "|" << setw(9) << OurPatients[0].homeAddress.apartment << endl;;
	I++;
    file_out.close();
}

void head() {
    file_out.open(PATH, ios_base::out);
	file_out << left << setw(3) << "N" << "|" << setw(15) << "Surname" << "|" << setw(10) << "Name" << "|" << setw(15) << "Last name" << "|"
	     		<< setw(6) << "Gender" << "|" << setw(15) << "Nationality" << "|" << setw(6) << "Growth" << "|"
				<< setw(6) << "Weight" << "|" << setw(10) << "Date" << "|" << setw(13) << "Phone number" << "|"
				<< setw(15) << "Hospital number" << "|" << setw(6) << "Branch" << "|" << setw(19) << "Medical card number" << "|"
				<< setw(15) << "Diagnosis" << "|" << setw(10) << "Blood type" << "|" 
                << setw(8) << "Zip code" << "|" << setw(10) << "Country" << "|" << setw(10) << "Region" << "|"
				<< setw(10) << "District" << "|" << setw(10) << "City" << "|" << setw(20) << "Street" << "|"
				<< setw(5) << "House" << "|" << setw(9) << "Apartment" << endl;
    file_out.close();
}

void add() {
	create();
}

void remove() {
    cout <<"Enter the line number to delete: "<< endl;
    int lineNumberToDelete;
    cin >> lineNumberToDelete;

	file_in.open(PATH, ios_base::in);
    string s, sum_s = "";
    int i = 0;
    while (getline(file_in, s)) { 
        i++;
        if (i == 1 || i == 2) continue;
        if (i - 2 == lineNumberToDelete) continue;
        sum_s += s + "\n";
    }
    file_in.close();

    head();
    file_out.open(PATH, ios_base::app);
    file_out << sum_s;
    file_out.close();
}

void sort() {
    /**/
	




// Функция, получающая строки файла в виде списка типа string*
// Параметры:
// - filename - имя файла;
// - _lines - список строк файла типа (string*).
// Функция возвращает общее количество прочитанных строк.
int GetStringsFromFileS(string filename, string** _lines)
{
  // 1. Дополнительные переменные
  string* lines; // временный список строк
  int n = CountLinesInFile(filename); // Получить количество строк в файле

  // 2. Проверка, правильно ли прочитаны строки из файла
  if (n == -1) return -1;

  // 3. Объявить файловую переменную и открыть файл filename для чтения
  ifstream F(filename);

  // 4. Проверка, открыт ли файл
  if (!F) return -1;

  // 5. Попытка выделить память для n строк типа string
  try
  {
    lines = new string[n];
  }
  catch (bad_alloc e)
  {
    cout << e.what() << endl; // вывести сообщение об ошибке
    F.close();
    return -2; // возврат с кодом -2
  }

  // 6. Чтение строк из файла и запись строк в список lines
  char buffer[1000]; // буфер для чтения строки

  for (int i = 0; i < n; i++)
  {
    // 6.1. Прочитать строку из файла в буфер buffer
    F.getline(buffer, 1000);

    // 6.2. Вычислить длину прочитанной строки
    int len;
    for (len = 0; buffer[len] != '\0'; len++);

    // 6.3. Записать buffer => lines[i], использовать метод assign().
    // Скопировать len байт из buffer в lines[i].
    lines[i].assign(buffer, len);
  }

  // 7. Закрыть файл
  F.close();

  // 8. Вернуть результат
  *_lines = lines;
  return n;
}
Использование функции GetStringsFromFileS() может быть, например, следующим

void main()
{
  // Вывод списка строк файла на экран
  // 1. Объявить внутренние переменные
  int count; // количество строк
  string* lines = nullptr; // список строк типа string

  // 2. Получить список строк типа string*
  count = GetStringsFromFileS("TextFile1.txt", &lines);

  // 3. Проверка, получен ли список
  if (count < 0)
  {
    cout << "Error" << endl;
    return;
  }

  // 3. Вывести список строк на экран
  for (int i = 0; i < count; i++)
  {
    cout << lines[i] << endl;
  }

  // 4. Освободить память, выделенную для массива lines
  if (lines != nullptr)
    delete[] lines;
}
}

Patient* AddStruct() {
	if (amount == 0) {
		OurPatients = new Patient[amount + 1];
	}
	else {
		Patient* tempOurPatients = new Patient[amount + 1];

		for (int i = 0; i < amount; i++) {
			tempOurPatients[i] = OurPatients[i];
		}
		delete [] OurPatients;
		OurPatients = tempOurPatients;
	}
	return OurPatients;
}

void setData() {
	cout << "Surname: ";
	cin >> OurPatients[amount].surname;

	cout << "Name: ";
	cin >> OurPatients[amount].name;

	cout << "Last name: ";
	cin >> OurPatients[amount].lastName;

	cout << "Gender (m/f): ";
	cin >> OurPatients[amount].sex;

	cout << "Nationality: ";
	cin >> OurPatients[amount].nationality;

	cout << "Growth: ";
	cin >> OurPatients[amount].growth;
	cin.get();

	cout << "Weight: ";
	cin >> OurPatients[amount].weight;
	cin.get();

	cout << "Date of birth (year, month, day): ";
	year:
	cin >> OurPatients[amount].dateOfBirth.year;
	if(OurPatients[amount].dateOfBirth.year < 1900) {
		cout << "Enter the normal year! >>";
		goto year;
	}
	month:
	cin >> OurPatients[amount].dateOfBirth.month;
	if(OurPatients[amount].dateOfBirth.month > 12 || OurPatients[amount].dateOfBirth.month < 1) {
		cout << "Enter the normal month! >>";
		goto month;
	}
	cin >> OurPatients[amount].dateOfBirth.day;
	cin.get();
	
	cout << "Phone number: ";
	cin >> OurPatients[amount].phoneNumber;

	cout << "Home address (zip code, country, region, district, city, street, house, apartment): \n";
	cin >> OurPatients[amount].homeAddress.zipCode;
	cin >> OurPatients[amount].homeAddress.country;
	cin >> OurPatients[amount].homeAddress.region;
	cin >> OurPatients[amount].homeAddress.district;
	cin >> OurPatients[amount].homeAddress.city;
	cin >> OurPatients[amount].homeAddress.street;
	cin >> OurPatients[amount].homeAddress.house;
	cin >> OurPatients[amount].homeAddress.apartment;
	cin.get();

	cout << "Hospital number: ";
	cin >> OurPatients[amount].hospitalNumber;
	cin.get();

	cout << "Branch: ";
	cin >> OurPatients[amount].branch;

	cout << "Medical card number: ";
	cin >> OurPatients[amount].medicalCardNumber;
	cin.get();

	cout << "Diagnosis: ";
	cin >> OurPatients[amount].diagnosis;

	cout << "Blood type: ";
	cin >> OurPatients[amount].bloodType;

	cout << endl;
}