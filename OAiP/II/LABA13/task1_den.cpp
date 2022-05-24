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

struct Buyer {
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

	int creditCardNumber = 0;
	int bankAccountNumber = 0;
};

void create();
void viewing();
void add();
void remove();
void sort();

int menu();
void(*masf[])() = {create, viewing, add, remove, sort};

Buyer* AddStruct();
void setData();
void recording();
void head();

int amount = 0;
int I = 0;
Buyer* OurBuyers = new Buyer[0];
string PATH = "file1.txt";
ofstream file_out;
ifstream file_in;
int main() {
    head();
	while(1) (*masf[menu()])();

    try {
        delete[] OurBuyers;
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
		OurBuyers = AddStruct();
		setData();

		amount++;

		cout << "Continue entering data (1 - yes, 0 - no)?";
		cin >> YesOrNot;
		cin.get();
        recording();
        delete[] OurBuyers;
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

	
	file_out << left << setw(3) << I + 1 << "|" << setw(15) << OurBuyers[0].surname << "|" 
				<< setw(10) << OurBuyers[0].name << "|" << setw(15) << OurBuyers[0].lastName << "|"
	     		<< setw(6) << OurBuyers[0].sex << "|" << setw(15) << OurBuyers[0].nationality << "|" 
				<< setw(6) << OurBuyers[0].growth << "|" << setw(6) << OurBuyers[0].weight << "|"
				<< setw(2) << OurBuyers[0].dateOfBirth.day << "." 
				<< setw(2) << OurBuyers[0].dateOfBirth.month << "." << setw(4) << OurBuyers[0].dateOfBirth.year << "|" 
				<< setw(13) << OurBuyers[0].phoneNumber << "|"  << setw(19) << OurBuyers[0].creditCardNumber << "|" 
				<< setw(19) << OurBuyers[0].bankAccountNumber << "|" 
	     		<< setw(8) << OurBuyers[0].homeAddress.zipCode << "|" << setw(10) << OurBuyers[0].homeAddress.country << "|"
				<< setw(10) << OurBuyers[0].homeAddress.region << "|" << setw(10) << OurBuyers[0].homeAddress.district << "|"
				<< setw(10) << OurBuyers[0].homeAddress.city << "|" << setw(20) << OurBuyers[0].homeAddress.street << "|"
				<< setw(5) << OurBuyers[0].homeAddress.house << "|" << setw(9) << OurBuyers[0].homeAddress.apartment << endl;
	I++;
    file_out.close();
}

void head() {
    file_out.open(PATH, ios_base::out);
	file_out << left << setw(3) << "N" << "|" << setw(15) << "Surname" << "|" << setw(10) << "Name" << "|" << setw(15) << "Last name" << "|"
	     		<< setw(6) << "Gender" << "|" << setw(15) << "Nationality" << "|" << setw(6) << "Growth" << "|"
				<< setw(6) << "Weight" << "|" << setw(10) << "Date" << "|" << setw(13) << "Phone number" << "|"
				<< setw(19) << "Credit card number" << "|" << setw(19) << "Bank account number" << "|" 
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
    cout << "Not working";
    system("pause");
}

Buyer* AddStruct() {
	if (amount == 0) {
		OurBuyers = new Buyer[amount + 1];
	}
	else {
		Buyer* tempOurBuyers = new Buyer[amount + 1];

		for (int i = 0; i < amount; i++) {
			tempOurBuyers[i] = OurBuyers[i];
		}
		delete [] OurBuyers;
		OurBuyers = tempOurBuyers;
	}
	return OurBuyers;
}
void setData() {
	cout << "Surname: ";
	cin >> OurBuyers[amount].surname;

	cout << "Name: ";
	cin >> OurBuyers[amount].name;

	cout << "Last name: ";
	cin >> OurBuyers[amount].lastName;

	cout << "Gender (m/f): ";
	cin >> OurBuyers[amount].sex;

	cout << "Nationality: ";
	cin >> OurBuyers[amount].nationality;

	cout << "Growth: ";
	cin >> OurBuyers[amount].growth;
	cin.get();

	cout << "Weight: ";
	cin >> OurBuyers[amount].weight;
	cin.get();

	cout << "Date of birth (year, month, day): ";
	cout << "Date of birth (year, month, day): ";
	year:
	cin >> OurBuyers[amount].dateOfBirth.year;
	if(OurBuyers[amount].dateOfBirth.year < 1900) 
	{
		cout << "Enter the normal year! >>";
		goto year;
	}
	month:
	cin >> OurBuyers[amount].dateOfBirth.month;
	if(OurBuyers[amount].dateOfBirth.month > 12 || OurBuyers[amount].dateOfBirth.month < 1) 
	{
		cout << "Enter the normal month! >>";
		goto month;
	}
	cin >> OurBuyers[amount].dateOfBirth.day;
	cin.get();
	
	cout << "Phone number: ";
	cin >> OurBuyers[amount].phoneNumber;

	cout << "Home address (zip code, country, region, district, city, street, house, apartment): \n";
	cin >> OurBuyers[amount].homeAddress.zipCode;
	cin >> OurBuyers[amount].homeAddress.country;
	cin >> OurBuyers[amount].homeAddress.region;
	cin >> OurBuyers[amount].homeAddress.district;
	cin >> OurBuyers[amount].homeAddress.city;
	cin >> OurBuyers[amount].homeAddress.street;
	cin >> OurBuyers[amount].homeAddress.house;
	cin >> OurBuyers[amount].homeAddress.apartment;
	cin.get();

	cout << "Credit card number: ";
	cin >> OurBuyers[amount].creditCardNumber;
	cin.get();

	cout << "Bank account number: ";
	cin >> OurBuyers[amount].bankAccountNumber;
	cin.get();

	cout << endl;
}