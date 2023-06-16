#include <iostream>
#include <string>

class Sum
{
public:
    int add(int a, int b)
    {
        return a + b;
    }
    int add(int a, int b, float c)
    {
        return a + b + (int) c;
    }
    int add(int a, int b, int c)
    {
        return a + b + c;
    }  
};

class Cars
{
public:
    void print()
    {
        std::cout << "I am a car" << std::endl;
    }
    void print(int a)
    {
        std::cout << "I am a car with " << a << " wheels" << std::endl;
    }
    void print(int a, int b)
    {
        std::cout << "I am a car with " << a << " wheels and " << b << " doors" << std::endl;
    }
};

class Calculator
{
public:
    int operation (int a, int b, char op)
    {
        if (op == '+')
            return a + b;
        else if (op == '-')
            return a - b;
        else if (op == '*')
            return a * b;
        else if (op == '/')
            return a / b;
        else
            return 0;
    }

    int operation (int a, char op)
    {
        if (op == '!')
            return factorial(a);
        else
            return 0;
    }

    int operation (float a, float b)
    {
        return 0;
    }
private:
    int factorial (int a)
    {
        if (a == 0)
            return 1;
        else
            return a * factorial(a - 1);
    }
};

int main()
{
    Sum sum;
    std::cout << sum.add(1, 2) << std::endl;
    std::cout << sum.add(1, 2, 3) << std::endl;
    std::cout << sum.add(1, 2, 3) << std::endl;

    Cars car;
    car.print();
    car.print(4);
    car.print(4, 2);

    Calculator calc;
    std::cout << calc.operation(1, 2, '+') << std::endl;
    std::cout << calc.operation(1, 2, '-') << std::endl;
    std::cout << calc.operation(1, 2, '*') << std::endl;
    std::cout << calc.operation(1, 2, '/') << std::endl;
    std::cout << calc.operation(1, '!') << std::endl;
    std::cout << calc.operation(1.0f, 2.0f) << std::endl;

    return 0;
}