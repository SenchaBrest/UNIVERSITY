#include <iostream>
#include <windows.h>
#include <string>
#include <iomanip>
using namespace std;

struct Date
{
	int year = 0;
	int month = 0;
	int day = 0;
};

struct Address
{
	int zipCode = 0;
	string country;
	string region;
	string district;
	string city;
	string street;
	int house = 0;
	int apartment = 0;
};

struct Patient
{
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
void search();
void sort();

int menu();
void(*masf[])() = {create, viewing, add, search, sort};

Patient* AddStruct();
void setData();


int amount = 0;
Patient* OurPatients = new Patient[0];
int main(int argc, char* argv[])
{
	if (argc != 2)
	{
        cout << "You forgot to enter your name.\n";
        system("pause>null");
        exit(0);
    }
    else
	{
		cout << "Hi, " << argv[argc - 1] << "! Let's start!" << endl;
    }	

	while(1) (*masf[menu()])();
}
int menu()
{
	char n;
	do
	{	
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
void create()
{
	int YesOrNot = 0;
	do
	{
		OurPatients = AddStruct();
		setData();

		amount++;

		cout << "Continue entering data (1 - yes, 0 - no)?";
		cin >> YesOrNot;
		cin.get();
	} while (YesOrNot != 0);
}
void viewing()
{
	system("cls");
	cout << left << setw(3) << "N" << "|" << setw(15) << "Surname" << "|" << setw(10) << "Name" << "|" << setw(15) << "Last name" << "|"
	     		<< setw(6) << "Gender" << "|" << setw(15) << "Nationality" << "|" << setw(6) << "Growth" << "|"
				<< setw(6) << "Weight" << "|" << setw(10) << "Date" << "|" << setw(13) << "Phone number" << "|"
				<< setw(15) << "Hospital number" << "|" << setw(6) << "Branch" << "|" << setw(19) << "Medical card number" << "|"
				<< setw(15) << "Diagnosis" << "|" << setw(10) << "Blood type" << endl;
	for(int i = 1; i <= 164; i++)
	{
		cout << "=";
	}
	cout << endl;

	for (int i = 0; i < amount; i++)
	{
		cout << left << setw(3) << i + 1 << "|" << setw(15) << OurPatients[i].surname << "|" 
				<< setw(10) << OurPatients[i].name << "|" << setw(15) << OurPatients[i].lastName << "|"
	     		<< setw(6) << OurPatients[i].sex << "|" << setw(15) << OurPatients[i].nationality << "|" 
				<< setw(6) << OurPatients[i].growth << "|" << setw(6) << OurPatients[i].weight << "|"
				<< setw(2) << OurPatients[i].dateOfBirth.day << "." 
				<< setw(2) << OurPatients[i].dateOfBirth.month << "." << setw(4) << OurPatients[i].dateOfBirth.year
				<< "|" << setw(13) << OurPatients[i].phoneNumber << "|" << setw(15) << OurPatients[i].hospitalNumber << "|" 
				<< setw(6) << OurPatients[i].branch << "|" << setw(19) << OurPatients[i].medicalCardNumber << "|"
				<< setw(15) << OurPatients[i].diagnosis << "|" << setw(10) << OurPatients[i].bloodType << endl;
	}

	int YesOrNot = 0;
	cout << "Do you want to see information about the place of residence (1 - yes, 0 - no)?";
	cin >> YesOrNot;
	cin.get();
	if (YesOrNot == 1)
	{
		system("cls");
		cout << left << setw(3) << "N" << "|" << setw(15) << "Surname" << "|" << setw(10) << "Name" << "|" << setw(15) << "Last name" << "|"
	     		<< setw(8) << "Zip code" << "|" << setw(10) << "Country" << "|" << setw(10) << "Region" << "|"
				<< setw(10) << "District" << "|" << setw(10) << "City" << "|" << setw(20) << "Street" << "|"
				<< setw(5) << "House" << "|" << setw(9) << "Apartment" << endl;
		for(int i = 1; i <= 164; i++)
		{
			cout << "=";
		}
		cout << endl;

		for (int i = 0; i < amount; i++)
		{
			cout << left << setw(3) << i + 1 << "|" << setw(15) << OurPatients[i].surname << "|"
				<< setw(10) << OurPatients[i].name << "|" << setw(15) << OurPatients[i].lastName << "|"
	     		<< setw(8) << OurPatients[i].homeAddress.zipCode << "|" << setw(10) << OurPatients[i].homeAddress.country << "|"
				<< setw(10) << OurPatients[i].homeAddress.region << "|" << setw(10) << OurPatients[i].homeAddress.district << "|"
				<< setw(10) << OurPatients[i].homeAddress.city << "|" << setw(20) << OurPatients[i].homeAddress.street << "|"
				<< setw(5) << OurPatients[i].homeAddress.house << "|" << setw(9) << OurPatients[i].homeAddress.apartment << endl;
		}
	}
}
void add() 
{
	create();
}
void search() 
{
	string str;
	cout << "Search: ";
	cin >> str;

	int k = 0;
	for (int i = 0; i < amount; i++)
	{
		if (str == OurPatients[i].surname || str == OurPatients[i].name
			|| str == OurPatients[i].lastName)
		{
			system("cls");
			cout << left <<setw(3) << "N" << "|" << setw(15) << "Surname" << "|" << setw(10) << "Name" << "|" << setw(15) << "Last name" << "|"
	     		<< setw(6) << "Gender" << "|" << setw(15) << "Nationality" << "|" << setw(6) << "Growth" << "|"
				<< setw(6) << "Weight" << "|" << setw(10) << "Date" << "|" << setw(13) << "Phone number" << "|"
				<< setw(15) << "Hospital number" << "|" << setw(6) << "Branch" << "|" << setw(19) << "Medical card number" << "|"
				<< setw(15) << "Diagnosis" << "|" << setw(10) << "Blood type" << endl;
			for(int i = 1; i <= 164; i++)
			{
				cout << "=";
			}
			cout << endl;

	
			cout << left << setw(3) << i + 1 << "|" << setw(15) << OurPatients[i].surname << "|" 
				<< setw(10) << OurPatients[i].name << "|" << setw(15) << OurPatients[i].lastName << "|"
	     		<< setw(6) << OurPatients[i].sex << "|" << setw(15) << OurPatients[i].nationality << "|" 
				<< setw(6) << OurPatients[i].growth << "|" << setw(6) << OurPatients[i].weight << "|"
				<< setw(2) << OurPatients[i].dateOfBirth.day << "." 
				<< setw(2) << OurPatients[i].dateOfBirth.month << "." << setw(4) << OurPatients[i].dateOfBirth.year
				<< "|" << setw(13) << OurPatients[i].phoneNumber << "|" << setw(15) << OurPatients[i].hospitalNumber << "|" 
				<< setw(6) << OurPatients[i].branch << "|" << setw(19) << OurPatients[i].medicalCardNumber << "|"
				<< setw(15) << OurPatients[i].diagnosis << "|" << setw(10) << OurPatients[i].bloodType << endl;
	

			int YesOrNot = 0;
			cout << "Do you want to see information about the place of residence (1 - yes, 0 - no)?";
			cin >> YesOrNot;
			cin.get();
			if (YesOrNot == 1)
			{
				system("cls");
				cout << left << setw(3) << "N" << "|" << setw(15) << "Surname" << "|" << setw(10) << "Name" << "|" << setw(15) << "Last name" << "|"
	     			<< setw(8) << "Zip code" << "|" << setw(10) << "Country" << "|" << setw(10) << "Region" << "|"
					<< setw(10) << "District" << "|" << setw(10) << "City" << "|" << setw(20) << "Street" << "|"
					<< setw(5) << "House" << "|" << setw(9) << "Apartment" << endl;
				for(int i = 1; i <= 164; i++)
				{
					cout << "=";
				}
				cout << endl;

		
				cout << left << setw(3) << i + 1 << "|" << setw(15) << OurPatients[i].surname << "|"
				<< setw(10) << OurPatients[i].name << "|" << setw(15) << OurPatients[i].lastName << "|"
	     		<< setw(8) << OurPatients[i].homeAddress.zipCode << "|" << setw(10) << OurPatients[i].homeAddress.country << "|"
				<< setw(10) << OurPatients[i].homeAddress.region << "|" << setw(10) << OurPatients[i].homeAddress.district << "|"
				<< setw(10) << OurPatients[i].homeAddress.city << "|" << setw(20) << OurPatients[i].homeAddress.street << "|"
				<< setw(5) << OurPatients[i].homeAddress.house << "|" << setw(9) << OurPatients[i].homeAddress.apartment << endl;
		
	}
		}
		else
		{
			k += 1;
		}
	}
	if (k == amount)
	{
		cout << "Result not found.\n" << endl;
	}
}
void sort() 
{
	Patient buffer;
	for (int i = 0; i < amount - 1; i++) {
		for (int j = 0; j < amount - i - 1; j++) {
			if (OurPatients[j].surname > OurPatients[j + 1].surname) {
				buffer = OurPatients[j];
				OurPatients[j] = OurPatients[j + 1];
				OurPatients[j + 1] = buffer;
			}
		}
	}
}

Patient* AddStruct()
{
	if (amount == 0)
	{
		OurPatients = new Patient[amount + 1];
	}
	else
	{
		Patient* tempOurPatients = new Patient[amount + 1];

		for (int i = 0; i < amount; i++)
		{
			tempOurPatients[i] = OurPatients[i];
		}
		delete [] OurPatients;
		OurPatients = tempOurPatients;
	}
	return OurPatients;
}

void setData()
{
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
	if(OurPatients[amount].dateOfBirth.year < 1900) 
	{
		cout << "Enter the normal year! >>";
		goto year;
	}
	month:
	cin >> OurPatients[amount].dateOfBirth.month;
	if(OurPatients[amount].dateOfBirth.month > 12 || OurPatients[amount].dateOfBirth.month < 1) 
	{
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