#include <iostream>
#include <windows.h>
#include <string>
#include <iomanip>
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
void search();
void sort();

int menu();
void(*masf[])() = {create, viewing, add, search, sort};

Buyer* AddStruct();
void setData();

int amount = 0;
Buyer* OurBuyers = new Buyer[0];
int main(int argc, char* argv[]) {
	if (argc != 2) {
        cout << "You forgot to enter your name.\n";
        system("pause>null");
        exit(0);
    }
    else {
		cout << "Hi, " << argv[argc - 1] << "! Let's start!" << endl;
    }	

	while(1) (*masf[menu()])();
}

int menu() {
	char n;
	do {	
		cout << "\t   Menu\n";
		cout << "\t1. Create.\n";
		cout << "\t2. Viewing.\n";
		cout << "\t3. Add.\n";
		cout << "\t4. Search.\n";
		cout << "\t5. Sort.\n";
		cout << "\t6. Exit.\n";
		printf ("Make a choice: ");
		n = getchar();
		system("cls");
	}
	while(strchr("123456", n) == NULL);
	if(n == '6') exit(0);
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
	} while (YesOrNot != 0);
}
void viewing() {
	system("cls");
	cout << left << setw(3) << "N" << "|" << setw(15) << "Surname" << "|" << setw(10) << "Name" << "|" << setw(15) << "Last name" << "|"
	     		<< setw(6) << "Gender" << "|" << setw(15) << "Nationality" << "|" << setw(6) << "Growth" << "|"
				<< setw(6) << "Weight" << "|" << setw(10) << "Date" << "|" << setw(13) << "Phone number" << "|"
				<< setw(19) << "Credit card number" << "|" << setw(19) << "Bank account number" << endl;
	for(int i = 1; i <= 164; i++) {
		cout << "=";
	}
	cout << endl;

	for (int i = 0; i < amount; i++) {
		cout << left << setw(3) << i + 1 << "|" << setw(15) << OurBuyers[i].surname << "|" 
				<< setw(10) << OurBuyers[i].name << "|" << setw(15) << OurBuyers[i].lastName << "|"
	     		<< setw(6) << OurBuyers[i].sex << "|" << setw(15) << OurBuyers[i].nationality << "|" 
				<< setw(6) << OurBuyers[i].growth << "|" << setw(6) << OurBuyers[i].weight << "|"
				<< setw(2) << OurBuyers[i].dateOfBirth.day << "." 
				<< setw(2) << OurBuyers[i].dateOfBirth.month << "." << setw(4) << OurBuyers[i].dateOfBirth.year
				<< "|" << setw(13) << OurBuyers[i].phoneNumber << setw(19) << OurBuyers[i].creditCardNumber << "|" 
				<< setw(19) << OurBuyers[i].bankAccountNumber << endl;
	}

	int YesOrNot = 0;
	cout << "Do you want to see information about the place of residence (1 - yes, 0 - no)?";
	cin >> YesOrNot;
	cin.get();
	if (YesOrNot == 1) {
		system("cls");
		cout << left << setw(3) << "N" << "|" << setw(15) << "Surname" << "|" << setw(10) << "Name" << "|" << setw(15) << "Last name" << "|"
	     		<< setw(8) << "Zip code" << "|" << setw(10) << "Country" << "|" << setw(10) << "Region" << "|"
				<< setw(10) << "District" << "|" << setw(10) << "City" << "|" << setw(20) << "Street" << "|"
				<< setw(5) << "House" << "|" << setw(9) << "Apartment" << endl;
		for(int i = 1; i <= 164; i++) cout << "=";
		cout << endl;

		for (int i = 0; i < amount; i++) {
			cout << left << setw(3) << i + 1 << "|" << setw(15) << OurBuyers[i].surname << "|"
				<< setw(10) << OurBuyers[i].name << "|" << setw(15) << OurBuyers[i].lastName << "|"
	     		<< setw(8) << OurBuyers[i].homeAddress.zipCode << "|" << setw(10) << OurBuyers[i].homeAddress.country << "|"
				<< setw(10) << OurBuyers[i].homeAddress.region << "|" << setw(10) << OurBuyers[i].homeAddress.district << "|"
				<< setw(10) << OurBuyers[i].homeAddress.city << "|" << setw(20) << OurBuyers[i].homeAddress.street << "|"
				<< setw(5) << OurBuyers[i].homeAddress.house << "|" << setw(9) << OurBuyers[i].homeAddress.apartment << endl;
		}
	}
}

void add() {
	create();
}

void search() {
	string str;
	cout << "Search: ";
	cin >> str;

	int k = 0;
	for (int i = 0; i < amount; i++) {
		if (str == OurBuyers[i].surname || str == OurBuyers[i].name
			|| str == OurBuyers[i].lastName) {
			system("cls");
				cout << left << setw(3) << "N" << "|" << setw(15) << "Surname" << "|" << setw(10) << "Name" << "|" << setw(15) << "Last name" << "|"
	     		<< setw(6) << "Gender" << "|" << setw(15) << "Nationality" << "|" << setw(6) << "Growth" << "|"
				<< setw(6) << "Weight" << "|" << setw(10) << "Date" << "|" << setw(13) << "Phone number" << "|"
				<< setw(19) << "Credit card number" << "|" << setw(19) << "Bank account number" << endl;
			for(int i = 1; i <= 164; i++) cout << "=";
			cout << endl;

			for (int i = 0; i < amount; i++) {
				cout << left << setw(3) << i + 1 << "|" << setw(15) << OurBuyers[i].surname << "|" 
						<< setw(10) << OurBuyers[i].name << "|" << setw(15) << OurBuyers[i].lastName << "|"
			     		<< setw(6) << OurBuyers[i].sex << "|" << setw(15) << OurBuyers[i].nationality << "|" 
						<< setw(6) << OurBuyers[i].growth << "|" << setw(6) << OurBuyers[i].weight << "|"
						<< setw(2) << OurBuyers[i].dateOfBirth.day << "." 
						<< setw(2) << OurBuyers[i].dateOfBirth.month << "." << setw(4) << OurBuyers[i].dateOfBirth.year
						<< "|" << setw(13) << OurBuyers[i].phoneNumber << setw(19) << OurBuyers[i].creditCardNumber << "|" 
						<< setw(19) << OurBuyers[i].bankAccountNumber << endl;
			}
			int YesOrNot = 0;
			cout << "Do you want to see information about the place of residence (1 - yes, 0 - no)?";
			cin >> YesOrNot;
			cin.get();
			if (YesOrNot == 1) {
				system("cls");
				cout << left << setw(3) << "N" << "|" << setw(15) << "Surname" << "|" << setw(10) << "Name" << "|" << setw(15) << "Last name" << "|"
	     			<< setw(8) << "Zip code" << "|" << setw(10) << "Country" << "|" << setw(10) << "Region" << "|"
					<< setw(10) << "District" << "|" << setw(10) << "City" << "|" << setw(20) << "Street" << "|"
					<< setw(5) << "House" << "|" << setw(9) << "Apartment" << endl;
				for(int i = 1; i <= 164; i++) cout << "=";
				cout << endl;

				cout << left << setw(3) << i + 1 << "|" << setw(15) << OurBuyers[i].surname << "|"
				<< setw(10) << OurBuyers[i].name << "|" << setw(15) << OurBuyers[i].lastName << "|"
	     		<< setw(8) << OurBuyers[i].homeAddress.zipCode << "|" << setw(10) << OurBuyers[i].homeAddress.country << "|"
				<< setw(10) << OurBuyers[i].homeAddress.region << "|" << setw(10) << OurBuyers[i].homeAddress.district << "|"
				<< setw(10) << OurBuyers[i].homeAddress.city << "|" << setw(20) << OurBuyers[i].homeAddress.street << "|"
				<< setw(5) << OurBuyers[i].homeAddress.house << "|" << setw(9) << OurBuyers[i].homeAddress.apartment << endl;
			}
		}
		else k += 1;
	}
	if (k == amount) cout << "Result not found.\n" << endl;	
}

void sort() {
	Buyer buffer;
	for (int i = 0; i < amount - 1; i++) {
		for (int j = 0; j < amount - i - 1; j++) {
			if (OurBuyers[j].surname > OurBuyers[j + 1].surname) {
				buffer = OurBuyers[j];
				OurBuyers[j] = OurBuyers[j + 1];
				OurBuyers[j + 1] = buffer;
			}
		}
	}
}

Buyer* AddStruct() {
	if (amount == 0) OurBuyers = new Buyer[amount + 1];
	else {
		Buyer* tempOurBuyers = new Buyer[amount + 1];

		for (int i = 0; i < amount; i++) tempOurBuyers[i] = OurBuyers[i];
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