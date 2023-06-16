#include <iostream>
#include <string>

class Student 
{
private:
	std::string name;
	std::string surname;
	int dateOfBirthday[3];

public:
	Student()
	{
		this->name = "NoName";
		this->surname = "NoSurname";

		this->dateOfBirthday[0] = 1;
		this->dateOfBirthday[1] = 1;
		this->dateOfBirthday[2] = 2000;
	}

	Student(std::string name, std::string surname, int date[])
	{
		this->name = name;
		this->surname = surname;

		for (int i = 0; i < 3; i++)
		{
			this->dateOfBirthday[i] = date[i];
		}
		
	}

	Student(const Student &student)
	{
		this->name = student.name;
		this->surname = student.surname;

		for (int i = 0; i < 3; i++)
		{
			this->dateOfBirthday[i] = student.dateOfBirthday[i];
		}
	}
	
	void setName(std::string name) { this->name = name; }
	void setSurname(std::string surname) { this->surname = surname; }
	void setDateOfBirthday(int date[]) 
	{ 
		for (int i = 0; i < 3; i++)
		{
			this->dateOfBirthday[i] = date[i];
		}
	}

	std::string getName() { return this->name; }
	std::string getSurname() { return this->surname; }
	int* getDateOfBirthday() { return this->dateOfBirthday; }
	
	void operator=(const Student& student)
	{
		this->name = student.name;
		this->surname = student.surname;

		for (int i = 0; i < 3; i++)
		{
			this->dateOfBirthday[i] = student.dateOfBirthday[i];
		}
	}
	
	void operator--(int)
	{
		this->name = "NoName";
		this->surname = "NoSurname";
		
		this->dateOfBirthday[0] = 1;
		this->dateOfBirthday[1] = 1;
		this->dateOfBirthday[2] = 2000;
	}

	bool operator==(Student& obj)
	{
		return this->name == obj.name;
	}
};

int main()
{
	Student me;
	std::cout << me.getName() << "\n\n";

	int num[3] = { 9,9,2020 };
	Student T("ars","ki",num);
	std::cout << T.getName() << std::endl;
	T--;
	std::cout << T.getName() << "\n\n";

	std::cout << (me==T);

	return 0;
}