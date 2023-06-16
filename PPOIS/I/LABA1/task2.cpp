#include <iostream>
#include <string>

class ComplexNumbers
{
private:
	float a;
	float b;
public:
	ComplexNumbers()
	{
		this->a = 1;
		this->b = 1;
	}

	ComplexNumbers(float a, float b)
	{
		this->a = a;
		this->b = b;
	}

	ComplexNumbers(const ComplexNumbers& complexNumber)
	{
		this->a = complexNumber.a;
		this->b = complexNumber.b;
	}

	void setA(float a) { this->a = a; }
	void setB(float b) { this->b = b; }

	float getA() { return this->a; }
	float getB() { return this->b; }
	std::string getComplexNumberAsString()
	{ 
		std::string str;
		str = std::to_string(this->a);
		str.append(" + ");
		str.append(std::to_string(this->b));
		str.append("i");

		return str;
	}

	void operator=(const ComplexNumbers& complexNumber)
	{
		this->a = complexNumber.a;
		this->b = complexNumber.b;
	}

	ComplexNumbers operator+(const ComplexNumbers& complexNumber)
	{
		ComplexNumbers sum;
		sum.a = this->a + complexNumber.a;
		sum.b = this->b + complexNumber.b;
		return sum;
	}

	ComplexNumbers operator-(const ComplexNumbers& complexNumber)
	{
		ComplexNumbers difference;
		difference.a = this->a - complexNumber.a;
		difference.b = this->b - complexNumber.b;
		return difference;
	}

	ComplexNumbers operator*(const ComplexNumbers& complexNumber)
	{
		ComplexNumbers product;
		product.a = this->a * complexNumber.a - this->b * complexNumber.b;
		product.b = this->a * complexNumber.b + this->b * complexNumber.a;
		return product;
	}

	ComplexNumbers operator/(const ComplexNumbers& complexNumber)
	{
		ComplexNumbers quotient;
		quotient.a = (this->a * complexNumber.a + this->b * complexNumber.b) / \
		(complexNumber.a * complexNumber.a + complexNumber.b * complexNumber.b);
		quotient.b = (this->b * complexNumber.a - this->a * complexNumber.b) / \
		(complexNumber.a * complexNumber.a + complexNumber.b * complexNumber.b);
		return quotient;
	}

	bool operator==(ComplexNumbers& complexNumber)
	{
		return this->a == complexNumber.a && this->b == complexNumber.b;
	}
};

int main()
{
	ComplexNumbers a;
	std::cout << a.getA() << " + " << a.getB() << "i" << "\n\n";

	ComplexNumbers b(3,5);
	std::cout << b.getA() << " + " << b.getB() << "i" << "\n\n";

	std::cout << "Sum:" << (a + b).getA() << " + " << (a + b).getB() << "i" << "\n\n";
	std::cout << "Difference:" << (a - b).getA() << " + " << (a - b).getB() << "i" << "\n\n";
	std::cout << "Product:" << (a * b).getA() << " + " << (a * b).getB() << "i" << "\n\n";
	std::cout << "Quotient:" << (a / b).getA() << " + " << (a / b).getB() << "i" << "\n\n";	
}